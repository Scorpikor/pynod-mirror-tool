# -*- coding: utf-8 -*-
# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import configparser
import time
import os
from inc.class_tools import *
    

def log ( text, log_level):
    
    if generate_log_file == 1:
        if  log_level <= log_informativeness or log_level == 4:
            log_file.writelines(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} {text}\n")

    if log_level == 1:          # info
        if log_informativeness >= 1:
            text_line = TColor.GREEN + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text)
            print(text_line)
    if log_level == 2:          # info2
        if log_informativeness >= 2:
            text_line = TColor.CYAN + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text) 
            print(text_line)
            
    if log_level == 3:          # warning
        if log_informativeness >= 3:
            text_line = TColor.MAGENTA + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text)
            print(text_line)
            
    if log_level == 4:          # error
        text_line = TColor.RED + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text)
        print(text_line)
        
    if log_level == 5:          # debug
        if log_informativeness >= 5:
            text_line = TColor.YELLO + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text)
            print(text_line)
            

def trim_log_file_tail(path, max_bytes=1024*1024):
    # Функция обрезки лог файла если размер превышает max_bytes
    if not os.path.exists(path):
        return

    size = os.path.getsize(path)
    if size <= max_bytes:
        #log(f"Обрезка файла лога не нужна. Размер файла {size} <= {max_bytes}",2)
        return  # обрезка не нужна
        
    log(f"Производим обрезку файла лога....",3)
    with open(path, "rb") as f:
        f.seek(-max_bytes, os.SEEK_END)  # сдвигаемся назад от конца
        data = f.read()

        # Находим первую полную строку
        first_newline = data.find(b'\n')
        if first_newline != -1:
            data = data[first_newline + 1:]

    # Перезаписываем файл только этой частью
    with open(path, "wb") as f:
        f.write(data)

        
def close_log():
    if generate_log_file == 1:
        trim_log_file_tail(log_file_path, max_bytes=log_file_size*1024)
        log_file.writelines(f"\n"*5)
        log_file.close()

        
script_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(f"{script_root_dir}{os.sep}nod32ms.conf",encoding='utf-8')      # Считываем файл конфигурации nod32ms.conf
generate_log_file = int(config.get('LOG','generate_log_file'))
log_informativeness = int(config.get('LOG','log_informativeness'))
log_file_path = f"{script_root_dir}{os.sep}log.txt"             # Путь к лог файлу
log_file_size = int(config.get('LOG','log_file_size'))

if generate_log_file == 1:       
    log_file = open(log_file_path, "a", encoding='utf-8')
    trim_log_file_tail(log_file_path, max_bytes=log_file_size*1024)