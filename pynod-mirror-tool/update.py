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

if __name__ == "__main__":
    print("\n"*3)
    start_time = time.time()                                                    # Время запуска скрипта
    downloaded_size_all = 0                                                     # Счетчик сетевого трафика
    downloaded_files_all = 0                                                    # Счетчик скачанных файлов
    current_directory = os.path.dirname(os.path.abspath(__file__))              # Путь, из которого запускается update.py
    log("Текущая папка " + str(current_directory),5)
    os_platform,os_separator = os_dir_separator()                                     
    config = configparser.ConfigParser()
    config.read(current_directory + os_separator +'nod32ms.conf',encoding='utf-8')
    versions_to_update = parser_config_versions_to_update(current_directory + os_separator + 'nod32ms.conf')  # список версий баз антивируса для обновления
    official_servers_update = int(config.get('CONNECTION','official_servers_update'))
    connection_retry_probes = int(config.get('CONNECTION','mirror_connect_retries'))        # Kол-во попыток скачать файл
    web_server_root = str(config.get('SCRIPT','web_dir'))                                   # Путь к корню веб сервера, где будем хранить базы
    prefix_config = config.get('ESET','prefix')                                             # Имя папки, в которую складывать базы разных версий в корне веб сервера
    server_user = str(config.get('CONNECTION','mirror_user'))
    server_password = str(config.get('CONNECTION','mirror_password'))
    server_timeout = int(config.get('CONNECTION','mirror_timeout'))
    
    # ?????
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
        mirror_server = config.get('CONNECTION','mirror')                       # Сервер обновлений баз из конфига
        
    for version in versions_to_update:
        downloaded_size_version = 0                                             # Счетчик сетевого трафика для текущей версии
        downloaded_files_version = 0                                            # Счетчик скачанных файлов для текущей версии
        
        connect_dict = {
        'os_separator': os_separator,
        'current_directory': current_directory,
        'mirror_server':mirror_server,
        'retry_probes': connection_retry_probes,
        'server_user': server_user,
        'server_password': server_password,
        'server_timeout': server_timeout,
        'init_environment': init(version),
        'web_server_root': web_server_root,
        'prefix_config': prefix_config,
        }
        #print(connect_dict)
        download_av_base_version (version, connect_dict)
        
        
    