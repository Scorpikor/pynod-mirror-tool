# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import os
import configparser
import inspect
import sys
from inc.log import *

def parser_config_versions_to_update(config_file):
    # Парсим конфиг и возвращаем список версий антивируса, которые будем пытаться обновлять
    log("parser.py:parser_config_versions_to_update",5)
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    versions = []
    for key in config['ESET']:
        if 'version' in key:
            if config.get('ESET',key) == '1':
                versions.append(key[7::])
                
    return versions
    
def parser_update_ver(updatever_file_path):
    # Парсим update.ver и возвращаем список файлов для скачивания
    log("parser.py:parser_update_ver",5)
    files_to_download = []
    config = configparser.ConfigParser()
    config.read(updatever_file_path)
    for sect in config.sections():
        try:
            file = config.get(sect,'file')
            size = int(config.get(sect,'size'))
            files_to_download.append([file,size])
            
        except Exception as e:
            log("parser.py:parser_update_ver: В секции отсутствует file",5)
        
    log("parser.py:parser_update_ver: Необходимо скачать файлов: " + str(len(files_to_download)),5)
    return files_to_download     
    
def parser_get_DB_version(updatever_file):
    # узнаем версию баз в update.ver
    log("parser.py:get_DB_version",5)
    max = 0
    if os.path.exists(updatever_file):
    
        config = configparser.ConfigParser()    
        try:
            config.read(updatever_file)
            sections = config.sections()
        except Exception as e:
            return 0
            
        for section in sections:
            try:
                upd = config.get(section,'version').split()[0]
                if upd and float(upd) > max:
                    max = float(upd)
            except:
                log("parser.py:get_DB_version: Пропуск секции т.к. не содержит строку version",5)
        
    return max
    

    