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
from inc.web import *

if __name__ == "__main__":
    print("\n"*2)
    start_time = time.time()                                                    # Время запуска скрипта
    error_trigger = 0                                                           # Флаг ошибки
    error_text = []                                                             # Причины ошибок
    downloaded_size_all = 0                                                     # Счетчик сетевого трафика
    downloaded_files_all = 0                                                    # Счетчик скачанных файлов
    current_directory = os.path.dirname(os.path.abspath(__file__))              # Путь, из которого запускается update.py

    os_platform,os_separator = os_dir_separator()                               # Определяем платформу запуска и резделитель папок платформы
    log(f"Запущен скрипт {script_version(current_directory + os_separator)}",1)
    config = configparser.ConfigParser()
    config.read(current_directory + os_separator +'nod32ms.conf',encoding='utf-8')      # Считываем файл конфигурации nod32ms.conf
    versions_to_update = parser_config_versions_to_update(current_directory + os_separator + 'nod32ms.conf')  # список версий антивируса для обновления баз
    official_servers_update = int(config.get('CONNECTION','official_servers_update'))
    mirror_connect_retries = int(config.get('CONNECTION','mirror_connect_retries'))     # Kол-во попыток скачать файл
    max_workers = int(config.get('CONNECTION','max_workers'))                   # Кол-во потоков загрузки баз
    protoscan_v3_patch = int(config.get('PATCH','protoscan_v3_patch'))          # Триггер применения патча protoscan_v3_patch
    web_page_data = []                                                          # Для формирования WEB страницы отчета
    
    
    log(f"Используем платформу {os_platform}",3)
    log(f"Текущая папка {current_directory}",5)
    # Формируем путь web_server_root в зависимости от платформы (ОС)
    if os_platform == 'Linux':
        web_server_root = str(config.get('SCRIPT','linux_web_dir'))             # Путь к корню веб сервера, где будем хранить базы
    elif os_platform == 'Windows':
        web_server_root = str(config.get('SCRIPT','windows_web_dir'))
    elif os_platform == 'FreeBSD':
        web_server_root = str(config.get('SCRIPT','linux_web_dir'))
    else:
        log("Скрипт запущен на неопределенной платформе. Не понятно какие переменные для нее использовать.",4)
        log("Завершение работы скрипта....",4)
        sys.exit(1)
                                       
    prefix_config = os_separator + config.get('ESET','prefix')                  # Имя папки, в которую складывать базы разных версий в корне веб сервера
    server_user = str(config.get('CONNECTION','mirror_user'))
    server_password = str(config.get('CONNECTION','mirror_password'))
    server_timeout = int(config.get('CONNECTION','mirror_timeout'))
    
    # Выбор конфига init в соответствии с типом сервера, с которого обновляемся
    if official_servers_update == 1:
        from inc.init_official import *
        log("Режим обновления с официальных серверов (конфиг init_official.py)",1)
        oficial_servers = [value for key, value in config.items('OFFICIAL_SERVERS') if key.startswith('mirror')]
        # random
        random_version = random.choice(versions_to_update)
        file_get = init(random_version)['upd']
        random_useragent = user_agent(random_version)
        
        
        mirror, avg_time = choosing_the_best_server(oficial_servers, random_version, file_get, random_useragent )            # Выбор лучшего официального сервера для обновлений
        log("Выбран лучший официальный сервер для обновлений: " + str(mirror)+ " " + str(avg_time) +" ms",2)        
        mirror_server = f"http://{mirror}"
        #sys.exit(1)
    else:
        from inc.init import *
        log("Режим обновления с неофициальных зеркал (конфиг init.py)",1)
        mirror_server = str(config.get('CONNECTION','mirror'))                  # Сервер обновлений баз из конфига
        log(f"Сервер, с которого будем обновляться: {mirror_server}",2)
        
    log(f"\n",1)
    for version in versions_to_update:
        downloaded_size_version = 0                                             # Счетчик сетевого трафика для текущей версии
        downloaded_files_version = 0                                            # Счетчик скачанных файлов для текущей версии
        
        connect_dict = {
        'official_servers_update': official_servers_update,
        'os_separator': os_separator,
        'current_directory': current_directory,
        'mirror_server':mirror_server,
        'mirror_connect_retries': mirror_connect_retries,
        'max_workers' : max_workers,
        'server_user': server_user,
        'server_password': server_password,
        'server_timeout': server_timeout,
        'init_environment': init(version),
        'web_server_root': web_server_root,
        'prefix_config': prefix_config,
        'protoscan_v3_patch': protoscan_v3_patch,
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
        
        
        status_text = ""
        if result_dict['error'] != None:            
            log(f"[{version}] Ошибка скачивания баз версии" ,4)
            log(f"[{version}] Причина: {result_dict['error_text']}" ,4)
            error_trigger = 1                                                      # устанавливаем триггер ошибки
            # срезаем длинный текст ошибки
            error_string = result_dict['error_text']
            if len(error_string) > 250:
                try:
                    error_string = error_string.split('Ошибка:')[-1]
                except:
                    error_string = str(error_string[0:250]) + "..."
                    
            error_text.append(f"❌ [{version}] {error_text_fix(error_string)}")       # пишем сообщение  ошибки
            web_page_data.append([1,str(version),str(error_string),"","","","","","","",""])
            
            
        else:
            status_text = ""
            
            status_text += f"✅ [{version}] {result_dict['base_version']:g}\n"+\
                           f"Обновление : {upd_ver_creation_datetime}\n"+\
                           f"Размер базы: {sizeof_fmt(result_dict['full_size_dir'])} / {result_dict['full_number_of_files_dir']}ф\n"
                       
            if result_dict['retries_all'] != 0:
                status_text += f"           : ⚠️{result_dict['retries_all']} перезагрузок\n"
            
            status_text += f"Скачали    : {sizeof_fmt(result_dict['downloaded_size_versionown'])} / {result_dict['downloaded_files_version']}ф\n"
            
            #status_text += "</code>"    
                
            error_text.append(status_text)
            web_page_data.append([0,                                            # флаг ошибки
                                str(version),                                   # Версия антивируса
                                str(result_dict['base_version']),               # Версия баз
                                str(result_dict['retries_all']),                # Повторных загрузок
                                str(result_dict['downloaded_files_version']),   # Скачано файлов для базы текущей версии
                                str(sizeof_fmt(result_dict['downloaded_size_versionown'])),   # Размер скачанных файлов текущей версии
                                str(result_dict['trash_files_deleted']),        # Удалено
                                str(upd_ver_creation_datetime),                 # Базы обновились дата                                
                                str(update_date),                               # Последняя проверка дата
                                str(result_dict['full_number_of_files_dir']),   # файлов
                                str(sizeof_fmt(result_dict['full_size_dir'])),  # Размер базы
                                ])
            
            
            
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
        log(f"{'\n'*3}",1)


        
    end_time = str(convert_seconds(time.time() - start_time))
    full_base_size = (folder_size(web_server_root + prefix_config))
    log("-"*70,2)
    log(f"Всего скачано файлов        : {downloaded_files_all}",2)
    log(f"Размер всех скачанных файлов: {sizeof_fmt(downloaded_size_all)}",2)
    log(f"Полный размер всех баз {web_server_root + prefix_config} : {sizeof_fmt(full_base_size)}",2)
    log(f"Время выполнения скрипта: {end_time}" ,2)
    log("-"*70,2)
    print()
    web_page_data.append([0,"","","","","","","","","Скачано всего, файлов",str(downloaded_files_all)])
    web_page_data.append([0,"","","","","","","","","Скачано всего, размер",str(sizeof_fmt(result_dict['downloaded_size_versionown']))])
    web_page_data.append([0,"","","","","","","","","Полный размер всех баз",str(sizeof_fmt(full_base_size))])
    web_page_data.append([0,"","","","","","","","","Время выполнения скрипта",str(end_time)])
    
    if config.get('LOG','generate_web_page') == "1":
        web_page_generator(web_page_data,config.get('LOG','generate_table_only'),init_filepath_fix(os_separator,config.get('LOG','html_table_path_file')))
    
    # Формируем сообщение для Telegram
    if str(config.get('TELEGRAM','telegram_inform')) == "1":    
        info = ""
        token = config.get('TELEGRAM','token')
        chat_id = config.get('TELEGRAM','chat_id')
        if error_trigger == 0:
            msg_prefix = "✅"
        else:
            msg_prefix = "🆘"
        
        
        try:
            text = config.get('TELEGRAM','text').strip()
        except:
            text = ""
        if text !="":
            text += "\n"
            
        for txt in error_text:
            info +=f"{txt}\n"
                
        info += '<code>'+'-'*34 + "\n"
        info += f"Всего скачанно: {sizeof_fmt(downloaded_size_all)} / {downloaded_files_all}ф\n"
        info += f"Размер баз    : {sizeof_fmt(full_base_size)}\n"
        info += f"Скрипт работал: {end_time}\n"
        info += "</code>\n"
        
        
        t_msg = f"<code>{msg_prefix} {update_date}\n[Сервер: {platform.node()}]\n{text}\n{info}</code>"
        log(f"Кол-во символов в сообщении Telegram : {len(t_msg)}",3)
        send_msg(t_msg, token, chat_id)
    
    # Закрываем лог файл
    close_log()    
    
