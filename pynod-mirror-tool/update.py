# -*- coding: utf-8 -*-
# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import os
import time
import platform
import configparser
from inc.main import *
from inc.tools import *
from inc.parser import *
from inc.telegram import *
from inc.log import *

if __name__ == "__main__":
    print("\n"*3)
    start_time = time.time()                                                    # Время запуска скрипта
    error_trigger = 0                                                           # Флаг ошибки
    error_text = []                                                             # Причины ошибок
    downloaded_size_all = 0                                                     # Счетчик сетевого трафика
    downloaded_files_all = 0                                                    # Счетчик скачанных файлов
    current_directory = os.path.dirname(os.path.abspath(__file__))              # Путь, из которого запускается update.py
    log("Текущая папка " + str(current_directory),2)
    os_platform,os_separator = os_dir_separator()                               # Определяем платформу запуска и резделитель папок платформы
    config = configparser.ConfigParser()
    config.read(current_directory + os_separator +'nod32ms.conf',encoding='utf-8')
    versions_to_update = parser_config_versions_to_update(current_directory + os_separator + 'nod32ms.conf')  # список версий баз антивируса для обновления
    official_servers_update = int(config.get('CONNECTION','official_servers_update'))
    connection_retry_probes = int(config.get('CONNECTION','mirror_connect_retries'))        # Kол-во попыток скачать файл
    max_workers = int(config.get('CONNECTION','max_workers'))
    #
    if os_platform == 'Linux':
        web_server_root = str(config.get('SCRIPT','linux_web_dir'))             # Путь к корню веб сервера, где будем хранить базы
    elif os_platform == 'Windows':
        web_server_root = str(config.get('SCRIPT','windows_web_dir'))
    else:
        log("Скрипт запущен на неопределенной платформе. Не понятно какие переменные для нее использовать.",4)
        log("Завершение работы скрипта....",4)
        sys.exit(1)
                                       
    prefix_config = os_separator + config.get('ESET','prefix')                                             # Имя папки, в которую складывать базы разных версий в корне веб сервера
    server_user = str(config.get('CONNECTION','mirror_user'))
    server_password = str(config.get('CONNECTION','mirror_password'))
    server_timeout = int(config.get('CONNECTION','mirror_timeout'))
    
    # Выбор конфига init в соответствии с типом сервера
    if official_servers_update == 1:
        from inc.init_official import *
        log("Режим обновления с официальных серверов (init_official.py)",1)
        oficial_servers = [value for key, value in config.items('OFFICIAL_SERVERS') if key.startswith('mirror')]
        mirror, avg_time = choosing_the_best_server(oficial_servers)
        log("Выбран лучший официальный сервер для обновлений: " + str(mirror)+ " " + str(avg_time) +" ms",2)
        mirror_server ="http://" + str(mirror)        
    else:
        from inc.init import *
        log("Режим обновления с неофициальных зеркал (init.py)",1)
        mirror_server = str(config.get('CONNECTION','mirror'))                       # Сервер обновлений баз из конфига
        log("Сервер, с которого будем обновляться: " + mirror_server,2)
        
    for version in versions_to_update:
        downloaded_size_version = 0                                             # Счетчик сетевого трафика для текущей версии
        downloaded_files_version = 0                                            # Счетчик скачанных файлов для текущей версии
        
        connect_dict = {
        'os_separator': os_separator,
        'current_directory': current_directory,
        'mirror_server':mirror_server,
        'retry_probes': connection_retry_probes,
        'max_workers' : max_workers,
        'server_user': server_user,
        'server_password': server_password,
        'server_timeout': server_timeout,
        'init_environment': init(version),
        'web_server_root': web_server_root,
        'prefix_config': prefix_config,
        }
        
        result_dict = download_av_base_version (version, connect_dict)
        # =================
        # Формируем отчеты
        # =================
        
        # Текущая дата и время
        update_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        
        
        # Дата изменения update.ver
        try:
            upd_ver_creation_datetime = file_creation_datetime(f"{web_server_root}{os_separator}{init_filepath_fix(os_separator,init(version)['dll'])}") 
        except:
            upd_ver_creation_datetime = None
        
        if result_dict['error'] != None:
            error_trigger = 1                                                      # устанавливаем триггер ошибки
            # срезаем длинный текст ошибки
            error_string = result_dict['error_text']
            if len(error_string) > 250:
                try:
                    error_string = error_string.split('Ошибка:')[-1]
                except:
                    error_string = str(error_string[0:250]) + "..."
                    
            error_text.append(f"❌ [{version}] {error_text_fix(error_string)}")       # пишем сообщение  ошибки            
            log(f"Ошибка скачивания баз версии [{version}]" ,4)
            log(f"Причина: {result_dict['error_text']}" ,4)
        else:
            status_text = ""
            status_text += "<code>"\
            f"✅ [{version}] {result_dict['base_version']}\n"+\
            f"Последнее обновление : {upd_ver_creation_datetime}\n"+\
            f"Последняя проверка   : {update_date}\n"+\
            f"Файлов в базе версии : {result_dict['full_number_of_files_dir']}\n"+\
            f"Размер базы          : {sizeof_fmt(result_dict['full_size_dir'])}\n"
                       
            if result_dict['retries_all'] != 0:
                status_text += f"Повторных загрузок   : {result_dict['retries_all']} ⚠️\n"
            
            status_text += f"Скачали              : {sizeof_fmt(result_dict['downloaded_size_versionown'])}\n"
            status_text += f"Скачали файлов       : {result_dict['downloaded_files_version']}\n"
            
            status_text += "</code>"    
                
            error_text.append(status_text)
            
            
            
            
        downloaded_files_all += result_dict['downloaded_files_version']
        downloaded_size_all += result_dict['downloaded_size_versionown']
        
        log(f"{'-'*50}",2)
        log(f"Скачано файлов для базы текущей версии : {result_dict['downloaded_files_version']}",2)
        log(f"Размер скачанных файлов текущей версии : {sizeof_fmt(result_dict['downloaded_size_versionown'])}",2 )
        log(f"Кол-во старых файлов базы удалено      : {result_dict['trash_files_deleted']}",2 )
        log(f"Общее кол-во попыток перекачать файл   : {result_dict['retries_all']}",2)                
        log(f"Время скачивания баз версии [{version}]: {result_dict['update_time']}" ,2)
        log(f"Кол-во файлов в папке баз   [{version}]: {result_dict['full_number_of_files_dir']}" ,2)
        log(f"Размер папки с базами       [{version}]: {sizeof_fmt(result_dict['full_size_dir'])}" ,2)
        log(f"{'-'*50}",2)                
        print("\n"*3)
        


        
    end_time = str(convert_seconds(time.time() - start_time))
    full_base_size = (folder_size(web_server_root + prefix_config))
    log(TColor.CYAN +"-"*70 + TColor.ENDC,2)
    log(f"Всего скачано файлов        : {downloaded_files_all}",2)
    log(f"Размер всех скачанных файлов: {sizeof_fmt(downloaded_size_all)}",2)
    log(f"Полный размер всех баз {web_server_root + prefix_config} : {sizeof_fmt(full_base_size)}",2)
    log(f"Время выполнения скрипта: {end_time}" ,2)
    log(TColor.CYAN +"-"*70 + TColor.ENDC,2)
    print()
    # Отправка в телеграмм
    if str(config.get('TELEGRAM','telegram_inform')) == "1":    
        info = ""
        token = config.get('TELEGRAM','token')
        chat_id = config.get('TELEGRAM','chat_id')
        if error_trigger == 0:
            msg_prefix = "✅"
        else:
            msg_prefix = "🆘"
            
        for txt in error_text:
            info +=f"{txt}\n"
                
        info += '<code>'+'-'*43 + "\n"
        info += f"Всего скачано файлов        : {downloaded_files_all}\n"
        info += f"Размер всех скачанных файлов: {sizeof_fmt(downloaded_size_all)}\n"
        info += f"Полный размер всех баз      : {sizeof_fmt(full_base_size)}\n"
        info += f"Время выполнения скрипта    : {end_time}\n"
        info += "</code>\n"
        send_msg(f"{msg_prefix} {update_date} Сервер: {os.uname()[1]} \n\n {info}", token, chat_id)
        
    