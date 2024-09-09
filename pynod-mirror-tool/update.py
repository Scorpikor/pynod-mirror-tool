import time
import requests
import configparser
import os

from inc.init import *
from inc.tools import *
from inc.parser import *
from inc.user_agent import *

if __name__ == "__main__":
    download_size = 0
    downloaded_files = 0
    # Основная логика программы
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    start_time = time.time()
    config = configparser.ConfigParser()
    #config.sections()
    config.read(current_directory + '/nod32ms.conf')    
    versions_to_update = parser_config_versions_to_update(current_directory + '/nod32ms.conf')
    
    for version in versions_to_update:
        with requests.Session() as session:  # Создаём сессию
            init_environment = init(version) # Берем переменные для данной версии       
            print("Обновляем вериию:", version, init_environment['name'] )
            mirror = config.get('CONNECTION','mirror')
            mirror_dir = config.get('SCRIPT','web_dir')
        
            # Скачиваем update.ver
            download_dict = {
                'download_url': 'http://'+ mirror + '/'+ init_environment['upd'],   # Формируем URL на скачивание update.ver для данной версии
                'save_path': current_directory + '/tmp/update.ver',                   #mirror_dir + init_environment['dll'],                  # Путь, по которому сохраним update.ver
                'user_agent': user_agent(version),
                'server_user': config.get('CONNECTION','mirror_user'),
                'server_password': config.get('CONNECTION','mirror_password'),
                'server_timeout': int(config.get('CONNECTION','mirror_timeout'))       
                }
            print("Save PATH:", download_dict['save_path'])
            download_size = download_size + int(tools_download_file(session,download_dict)) #, proxy_sw, user, passwd
            downloaded_files = downloaded_files + 1
            # ============================================
            our_DB_version = get_DB_version(mirror_dir + init_environment['dll'])
            alien_DB_version = get_DB_version(download_dict['save_path'])
            print ("Версия баз у нас     :",our_DB_version)
            print ("Версия баз на зеркале:",alien_DB_version)
            if alien_DB_version == 0:
                print("Был скачан неправильный update.ver! Убедитесь, что на сервере есть базы для данной версии антивируса", version)
                print("Возможно, в init.py для данной версии", version, "неправильно указано значение словаря 'upd'")
                print("Продолжение выполнения скрипта невозможно!")
                sys.exit(0)
            if  our_DB_version >= alien_DB_version:
                print("Для версии антивируса", version, "обновление баз с зеркала", mirror, "не требуется")
            
            if  our_DB_version < alien_DB_version:
                print("Требуется обновление баз")
            
            
                #sys.exit(0)
                # ============================================
                files_to_download = parser_update_ver(download_dict['save_path'])
                for file in files_to_download:
                    download_dict = {
                    'download_url': 'http://'+ mirror + "/" + file,   # Формируем URL на скачивание update.ver для данной версии
                    'save_path': mirror_dir + '/' + file,        # Путь, по которому сохраним файл
                    'user_agent': user_agent(version),
                    'server_user': config.get('CONNECTION','mirror_user'),
                    'server_password': config.get('CONNECTION','mirror_password'),
                    'server_timeout': int(config.get('CONNECTION','mirror_timeout'))       
                    }
                    download_size = download_size + int(tools_download_file(session,download_dict))
                    downloaded_files = downloaded_files + 1
                
                move_file(current_directory + '/tmp/update.ver', mirror_dir + init_environment['dll']) 
            #print(versions_to_update)
            
            print(f"Скачано: {download_size/ (1024 * 1024):.2f} Мб" )
            print("Скачано файлов:", downloaded_files)
            session.close()
    # Конец
    end_time = time.time()
    print("Время выполнения скрипта: ", end_time - start_time)