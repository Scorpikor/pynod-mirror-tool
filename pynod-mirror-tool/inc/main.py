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

def download_av_base_version (version, connect_dict):
    # Скачиваем все файлы указанной версии
    downloaded_size_version = 0                                             # Счетчик сетевого трафика для текущей версии
    downloaded_files_version = 0                                            # Счетчик скачанных файлов для текущей версии
    os_separator = connect_dict['os_separator']
    
    with requests.Session() as session:                                     # Создаём сессию
            retries = Retry(total=connect_dict['retry_probes'],
                      backoff_factor=0.4,
                      status_forcelist=[ 429, 500, 502, 503, 504 ])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            
            init_environment = connect_dict['init_environment']                                    # Берем переменные для данной версии антивируса
            log("[" + str(version)+ "]" + " Обновляем вериию: " + str(init_environment['name']),1 )
             
            web_server_root = connect_dict['web_server_root']                     # Путь к корню веб сервера, где будем хранить базы
            prefix_config = connect_dict['prefix_config']                         # Имя папки, в которую складывать базы разных версий в корне веб сервера
            add_path =''        # добавочный путь
            new_files_list =[]                                                    # Список файлов новой базы (нужен для отчистки от старых файлов)
            
            # Скачиваем update.ver в tmp
            download_text = ' update.ver'
            download_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            download_dict = {
                'text': TColor.GREEN + "[" + download_time + "] " + TColor.ENDC + "[" + str(version)+ "]" + download_text,            # Текст в строке скачивания
                'download_url': connect_dict['mirror_server'] + '/'+ init_environment['upd'],                                         # Формируем URL на скачивание update.ver для данной версии
                'file_size': None,
                'save_path': connect_dict['current_directory'] + os_separator + 'tmp' + os_separator + 'update.ver',                  # Путь, по которому сохраним update.ver
                'user_agent': user_agent(version),                               # Юзер агент, для подключения к серверу
                'server_user': connect_dict['server_user'],                      # Логин для подключения к серверу
                'server_password': connect_dict['server_password'],              # Пароль для подключения к серверу
                'server_timeout': connect_dict['server_timeout']                 # Таймаут операций подключения   
                }
            print(download_dict)
            downloaded_size_version += int(tools_download_file(session,download_dict))
            #downloaded_files_version += 1

            session.close()