import os
import configparser
import inspect
import sys

def parser_config_versions_to_update(config_file):
    # Парсим конфиг и возвращаем список версий антивируса, которые будем пытаться обновлять
    config = configparser.ConfigParser()
    config.read(config_file)
    versions = []
    for key in config['ESET']:
        if 'version' in key:
            if config.get('ESET',key) == '1':
                versions.append(key[7::])
                
    return versions
    
def parser_update_ver(updatever_file_path):
    # Парсим update.ver и возвращаем список файлов для скачивания
    files_to_download = []
    config = configparser.ConfigParser()
    config.read(updatever_file_path)
    for sect in config.sections():
        try:
            file = config.get(sect,'file')
            if "/" not in file:
                #print("В конфиге только файл без пути") 
                # Пока не понятно когда формируются такие файлы. Вероятно, их формируют антивирусы, которые умеют создавать зеркало.
                file = "dll/" + file
                files_to_download.append(file)
            else:
                files_to_download.append(file)
        except Exception as e:
            print("В секции отсутствует file")
            #print(e)
        
    print("Надо скачать файлов:", len(files_to_download))
    return files_to_download     
    
def get_DB_version(updatever_file):
    # узнаем версию баз в update.ver
    max = 0
    if os.path.exists(updatever_file):
    
        config = configparser.ConfigParser()    
        try:
            config.read(updatever_file)
            sections = config.sections()
        except Exception as e:
            #print(e)
            return 0
            
        for section in sections:
            try:
                upd = config.get(section,'version').split()[0]
                if upd and float(upd) > max:
                    max = float(upd)
            except:
                print("Пропуск")
        
    return max
    

    
