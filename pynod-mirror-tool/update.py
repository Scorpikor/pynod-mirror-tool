# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool


import time
import requests
from requests.adapters import HTTPAdapter, Retry
import configparser
import os
import inspect
from inc.init import *
from inc.tools import *
from inc.parser import *
from inc.log import *
from inc.user_agent import *
from inc.class_tools import *

if __name__ == "__main__":
    print("")
    downloaded_size_all = 0                                                     # Счетчик сетевого трафика
    downloaded_files_all = 0                                                    # Счетчик скачанных файлов
    current_directory = os.path.dirname(os.path.abspath(__file__))              # Путь, из которого запускается update.py
    
    start_time = time.time()
    config = configparser.ConfigParser()
    config.read(current_directory + '/nod32ms.conf')    
    versions_to_update = parser_config_versions_to_update(current_directory + '/nod32ms.conf')  # список версий баз антивируса для обновления
    log("Текущая папка " + str(current_directory),5)
    
    for version in versions_to_update:
        downloaded_size_version = 0
        downloaded_files_version = 0
        with requests.Session() as session:                                     # Создаём сессию
            retries = Retry(total=config.get('CONNECTION','mirror_connect_retries'),
                backoff_factor=0.4,
                status_forcelist=[ 500, 502, 503, 504 ])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            
            init_environment = init(version)                                    # Берем переменные для данной версии антивируса     
            log("[" + str(version)+ "]" + " Обновляем вериию: " + str(init_environment['name']),1 )
            mirror_server = config.get('CONNECTION','mirror')                   # Сервер обновлений баз 
            web_server_root = config.get('SCRIPT','web_dir')                    # Путь к корню веб сервера, где будем хранить базы
            prefix_config = config.get('ESET','prefix')                         # Имя папки, в которую складывать базы разных версий в корне веб сервера
            add_path =''        # добавочный путь
            new_files_list =[]                                                  # Список файлов новой базы (нужен для отчистки от старых файлов)
                                    
            # Скачиваем update.ver в tmp
            download_text = ' update.ver'
            download_dict = {
                'text': TColor.GREEN + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + "[" + str(version)+ "]" + download_text,            # Текст в строке скачивания
                'download_url': mirror_server + '/'+ init_environment['upd'],               # Формируем URL на скачивание update.ver для данной версии
                'file_size': None,
                'save_path': current_directory + '/tmp/update.ver',                         # Путь, по которому сохраним update.ver
                'user_agent': user_agent(version),                                          # Юзер агент, для подключения к серверу
                'server_user': config.get('CONNECTION','mirror_user'),                      # Логин для подключения к серверу
                'server_password': config.get('CONNECTION','mirror_password'),              # Пароль для подключения к серверу
                'server_timeout': int(config.get('CONNECTION','mirror_timeout'))            # Таймаут операций подключения   
                }
            downloaded_size_version += int(tools_download_file(session,download_dict))
            downloaded_files_version += 1
            # ============================================
            our_DB_version = get_DB_version(web_server_root + '/' + init_environment['dll'])
            alien_DB_version = get_DB_version(download_dict['save_path'])
            log ("[" + str(version)+ "]" + " Версия баз у нас     : " + str(our_DB_version),1)
            log ("[" + str(version)+ "]" + " Версия баз на зеркале: " + str(alien_DB_version),1)
            if alien_DB_version == 0:
                log("Был скачан неправильный update.ver! Убедитесь, что на сервере есть базы для данной версии антивируса " + str(version),4)
                log("Возможно, в init.py для данной версии " + str(version) + " неправильно указано значение словаря 'upd'",4)
                log("Продолжение выполнения скрипта невозможно! Остановка скрипта.",4)
                sys.exit(0)
            if  our_DB_version >= alien_DB_version:
                log("[" + str(version)+ "]" + " Для версии антивируса " + str(version) + " обновление баз с зеркала " + str(mirror_server) + " не требуется",2)
            
            if  our_DB_version < alien_DB_version:
                log("[" + str(version)+ "]" + " Требуется обновление баз",2)
                files_to_download = parser_update_ver(download_dict['save_path'])
                num_files_to_download = len(files_to_download)
                add_path = ''
                file_counter = 0
                for file, size in files_to_download:
                    file_counter += 1
                    if not file.startswith("/"):
                        file = str(init_environment['fix']) + '/' + file                        
                        add_path = str(init_environment['fix'])
                    full_file_path = web_server_root + prefix_config + '/' + version + file
                    new_files_list.append([full_file_path,size])
                    download_text = " [" + str(file_counter) + "|" + str(num_files_to_download) + "]"   
                    download_dict = {
                    'text': TColor.GREEN + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + "[" + str(version)+ "]" + download_text,
                    'download_url': mirror_server + file,                                           # Формируем URL на скачивание update.ver для данной версии
                    'file_size': size,                                                              # Размер файла в байтах
                    'save_path': web_server_root + prefix_config + '/' + version + file,            # Путь, по которому сохраним файл
                    'user_agent': user_agent(version),
                    'server_user': config.get('CONNECTION','mirror_user'),
                    'server_password': config.get('CONNECTION','mirror_password'),
                    'server_timeout': int(config.get('CONNECTION','mirror_timeout'))       
                    }
                    download_result = int(tools_download_file(session,download_dict))
                    if download_result != 0:
                        downloaded_size_version += download_result
                        downloaded_files_version += 1
                    
                modify_update_ver(current_directory + '/tmp/update.ver',prefix_config + '/' + version + add_path)
                move_file(current_directory + '/tmp/update.ver', web_server_root + '/' + init_environment['dll'])
                DB_folder = web_server_root + prefix_config + '/' + version + add_path
                log("ПУТЬ К БАЗАМ : " + str(DB_folder),5)
                all_files_in_DB_folder = list_files_and_folders(DB_folder)
                files_to_delete = unique_elements([file_path[0] for file_path in new_files_list], all_files_in_DB_folder)
                
                delete_files(files_to_delete)                
                log("Кол-во старых файлов удалено: " + str(len(files_to_delete)),2)
                remove_empty_folders(DB_folder)
                log("Кол-во файлов в папке с базами " + str(version)+ ": " + str(len(all_files_in_DB_folder)),2)
                log("Размер папки c базами " + str(version)+ ": " + str(sizeof_fmt(folder_size(DB_folder))),2)           
            
            
            session.close()
            
            if our_DB_version != alien_DB_version:
                log("Успешно обновились с версии " + str(our_DB_version) + " до версии " + str(alien_DB_version),2)
            log("Скачано файлов для базы текущей версии : " + str(downloaded_files_version),2)
            log("Размер скачанных файлов текущей версии : " + str(sizeof_fmt(downloaded_size_version)),2 )
            downloaded_size_all += downloaded_size_version                                                      # Счетчик сетевого трафика
            downloaded_files_all += downloaded_files_version
            print("")
    # ---
    
    log(TColor.CYAN +"-"*70 + TColor.ENDC,2)
    log("Всего скачано файлов        : " + str(downloaded_files_all),2)
    log("Размер всех скачанных файлов: " + str(sizeof_fmt(downloaded_size_all)),2)
    log("Полный размер всех баз " + str(web_server_root) + str(config.get('ESET','prefix')) + ": " + str(sizeof_fmt(folder_size(web_server_root + config.get('ESET','prefix')))),2)
    for version in versions_to_update:
        DB_folder = web_server_root + prefix_config + '/' + version
        all_files_in_DB_folder = list_files_and_folders(DB_folder)
        message = f"[{str(version):<5}]" \
        f" Файлов в папке с базами: {str(len(all_files_in_DB_folder)):<6}" \
        f" Размер папки:  {str(sizeof_fmt(folder_size(DB_folder))):<8}"
        log(message,2)      
    
    end_time = time.time()
    log("Время выполнения скрипта: " + str(convert_seconds(end_time - start_time)),2)
    log(TColor.CYAN +"-"*70 + TColor.ENDC,2)