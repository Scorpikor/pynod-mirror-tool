# -*- coding: utf-8 -*-
# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import time
import requests
from requests.adapters import HTTPAdapter, Retry
from inc.log import *
from inc.user_agent import *
from inc.tools import *
from inc.parser import *

#from http import HTTPStatus
from requests.exceptions import HTTPError

def download_av_base_version (version, connect_dict):
    # Скачиваем все файлы указанной версии
    start_ver_time = time.time()
    downloaded_size_version = 0                                             # Счетчик сетевого трафика для текущей версии
    downloaded_files_version = 0                                            # Счетчик скачанных файлов для текущей версии
    os_separator = connect_dict['os_separator']                             # Разделитель папок, характерный для текущей ОС
    connect_user_agent = user_agent(version)                                # Формируем строку с юзерагентом
    retries_all = 0                                                         # Общее кол-во попыток перекачать файл
    alien_DB_version = 0
    our_DB_version = 0
    
    with requests.Session() as session:                                     # Создаём сессию
            retries = Retry(total=connect_dict['mirror_connect_retries'],
                      backoff_factor=0.4,
                      status_forcelist=[ 429, 500, 502, 503, 504 ])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            
            init_environment = connect_dict['init_environment']             # Берем переменные для данной версии антивируса
            log("[" + str(version)+ "]" + " Обновляем вериию: " + str(init_environment['name']),1 )
             
            web_server_root = connect_dict['web_server_root']               # Путь к корню веб сервера, где будем хранить базы
            prefix_config = connect_dict['prefix_config']                   # Имя папки, в которую складывать базы разных версий в корне веб сервера
            add_path = ''                                                   # добавочный путь
            new_files_list = []                                             # Список файлов новой базы (нужен для отчистки от старых файлов)
            files_to_delete = []                                            # Список старых файлов базы для удаления
            upd_ver_in_storage_path = f"{web_server_root}{os_separator}{init_filepath_fix(os_separator,init_environment['dll'])}"
            our_DB_version = parser_get_DB_version(upd_ver_in_storage_path)
            log (f"[{version}] В хранилище update.ver версии : {our_DB_version} {upd_ver_in_storage_path}",1)
            # ==========================
            # Скачиваем update.ver в tmp
            # ===========================
            log(f"Скачиваем файл update.ver ",2)
            download_text = ' update.ver'
            download_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            tmp_updatever_filepath = f"{connect_dict['current_directory']}{os_separator}tmp{os_separator}update.ver"
            log (f"[{version}] Сохраняем update.ver в  : {tmp_updatever_filepath}",1)
            # Словарь для скачивания update.ver
            download_dict = {
                'text': TColor.GREEN + "[" + download_time + "] " + TColor.ENDC + "[" + str(version)+ "]" + download_text,      # Текст в строке скачивания
                'colour': 'green',                                                                                              # Цвет пролосы скачивания
                'download_url': connect_dict['mirror_server'] + '/'+ init_environment['upd'],                                   # Формируем URL на скачивание update.ver для данной версии
                'file_size': None,
                'save_path': tmp_updatever_filepath,                                                                            # Путь, по которому сохраним update.ver
                'user_agent': connect_user_agent,                                                                               # Юзер агент, для подключения к серверу
                'server_user': connect_dict['server_user'],                                                                     # Логин для подключения к серверу
                'server_password': connect_dict['server_password'],                                                             # Пароль для подключения к серверу
                'server_timeout': connect_dict['server_timeout'],                                                               # Таймаут операций подключения
                'mirror_connect_retries': connect_dict['mirror_connect_retries']                                                                    # Кол-во попытак скачать файл
                }
            ####print(download_dict)
            # Ожидаем на выходе:
            # Ошибка, текст ошибки, размер скачанного файла, путь сохранения файла
            error, error_text, downloaded_size_version_result, path_to_save = tools_download_file(session, download_dict)
            if error == None:
                downloaded_size_version += downloaded_size_version_result
                downloaded_files_version += 1   # update.ver скачиваем всегда
            else:
                # формируем словарь для возврата
                end_ver_time = str(convert_seconds(time.time() - start_ver_time))
                save_path = connect_dict['web_server_root'] + prefix_config + os_separator + version
                ret_dict = {
                    'error': error,                                                     # 0 = нет ошибок
                    'error_text': error_text,                                           # текст ошибки если была
                    'downloaded_files_version': downloaded_files_version,                                                       # кол-во скачанных файлов для текущей версии
                    'downloaded_size_versionown': downloaded_size_version,                                          # размер скачанных файлов для текущей версии
                    'retries_all' : retries_all,                                                                                # кол-во попыток перекачать файл
                    'full_number_of_files_dir' : len(list_files_and_folders(save_path)),                                        # полное кол-во файлов в папке баз текущей версии
                    'full_size_dir':  folder_size(save_path),                                                       # полный размер файлов базы текущей версии
                    'trash_files_deleted': len(files_to_delete),                                                                # кол-во старых файлов удалено
                    'update_time': end_ver_time,                                                                                # время, затраченное на обновление баз текущей версии
                }            
                return ret_dict
            # ============================================
            # our_DB_version = parser_get_DB_version(web_server_root + os_separator + init_environment['dll'])
            alien_DB_version = parser_get_DB_version(download_dict['save_path'])
            log ("[" + str(version)+ "]" + " Версия баз у нас     : " + str(our_DB_version),1)
            log ("[" + str(version)+ "]" + " Версия баз на зеркале: " + str(alien_DB_version),1)
            
            save_path = connect_dict['web_server_root'] + prefix_config + os_separator + version    # Путь, по которому будем сохранять файлы базы без части из update.ver
            if alien_DB_version == 0:
                log("Был скачан неправильный update.ver! Убедитесь, что на сервере есть базы для данной версии антивируса " + str(version),4)
                log("Возможно, в init.py для данной версии " + str(version) + " неправильно указано значение словаря 'upd'",4)
                log("Продолжение выполнения скрипта невозможно! Остановка скрипта.",4)
                sys.exit(0)
            if  our_DB_version >= alien_DB_version:
                log("[" + str(version)+ "]" + " Для версии антивируса " + str(version) + " обновление баз с зеркала " + str(connect_dict['mirror_server']) + " не требуется",2)
            
            if  our_DB_version < alien_DB_version:
                # ================================
                log("[" + str(version)+ "]" + " Требуется обновление баз",2)
                
                files_to_download = parser_update_ver(download_dict['save_path'])
                num_files_to_download = len(files_to_download)
                log("[" + str(version)+ "]" + " Кол-во файлов в update.ver для загрузки: " + str(num_files_to_download) ,2)
                
                file_counter = 0
                                
                # =====================
                # Скачиваем файлы баз
                # =====================
                download_dict = {
                    'version': version,
                    'os_separator': os_separator,
                    'path_fix': str(init_environment['fix']),                    # правка пути если, например, обновляемся с зеркала, созданного самим антивирусом
                    'mirror_server': connect_dict['mirror_server'],              # Формируем URL на скачивание update.ver для данной версии
                    'save_path': save_path,                                      # Путь, по которому будем сохранять файлы базы без части из update.ver
                    'user_agent': connect_user_agent,                            # user-agent с которым подключаемся к серверу
                    'server_user': connect_dict['server_user'],                  # логин для подключения к серверу
                    'server_password': connect_dict['server_password'],          # пароль для подключения к серверу
                    'server_timeout': connect_dict['server_timeout'],            # таймаут операций скачивания
                    'mirror_connect_retries' : connect_dict['mirror_connect_retries'],     # кол-во попыток перекачать файл
                    'max_workers' : connect_dict['max_workers'],                 # кол-во потоков скачивания
                    }
                    
                # Ожидаем на выходе:
                # Ошибка, текст ошибки, размер скачанных файлов, кол-во скачанных файлов, общее кол-во попытак перекачать файл, список сохраненных файлов
                error, error_text, downloaded_size_version_result, downloaded_files_version_result, retries_all, new_files_list = download_files_concurrently(download_dict, files_to_download)
                if error != None:
                    log(f"[{version}] Не удалось обновить версию с {our_DB_version} до версии {alien_DB_version}",4)
                    
                else:
                    if our_DB_version != alien_DB_version:
                        log("Успешно обновились с версии " + str(our_DB_version) + " до версии " + str(alien_DB_version),2)
                        # Копируем update.ver в хранилище
                        updatever_storage_path = f"{connect_dict['web_server_root']}{os_separator}{init_filepath_fix(os_separator,init_environment['dll'])}"
                        log (f"[{version}] Перемещаем update.ver в хранилище : {updatever_storage_path}",1)
                        move_file(tmp_updatever_filepath, updatever_storage_path)
                        
                downloaded_size_version += downloaded_size_version_result
                downloaded_files_version += downloaded_files_version_result
                                                    
                log(f"Путь к базам : {download_dict['save_path']}",3)
                
                # Отчистка от старых файлов
                all_files_in_DB_folder = list_files_and_folders(download_dict['save_path'])
                files_to_delete = elements_to_delete(new_files_list, all_files_in_DB_folder)
                delete_files(files_to_delete)
                remove_empty_folders(download_dict['save_path'])                
                #log(f"Список файлов для удаления : {files_to_delete}",3)
                log(f"Кол-во старых файлов удалено : {len(files_to_delete)}",5)                
                
                
                
            session.close()
    end_ver_time = str(convert_seconds(time.time() - start_ver_time))
    # Возвращаем
    ret_dict = {
        'error': error,                                                         # None = нет ошибок
        'error_text': error_text,                                               # текст ошибки если была
        'base_version': alien_DB_version,                                       # версия баз 
        'downloaded_files_version': downloaded_files_version,                   # кол-во скачанных файлов для текущей версии
        'downloaded_size_versionown': downloaded_size_version,                  # размер скачанных файлов для текущей версии
        'retries_all' : retries_all,                                            # кол-во попыток перекачать файл
        'full_number_of_files_dir' : len(list_files_and_folders(save_path)),    # кол-во файлов в папке баз текущей версии
        'full_size_dir':  folder_size(save_path),                               # полный размер файлов базы текущей версии
        'trash_files_deleted': len(files_to_delete),                            # кол-во старых файлов удалено
        'update_time': end_ver_time,                                            # время, затраченное на обновление баз текущей версии
        }
        

    return ret_dict
    
    
    