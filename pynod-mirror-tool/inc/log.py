# -*- coding: utf-8 -*-
# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import configparser
import time
import os
import re
from inc.class_tools import *

if os.name == "nt":
    try:
        # Пробуем подключить colorama для правильного отображения цвета в терминале для windows ОС
        import colorama
        colorama.init(convert=True, autoreset=True)
    except ImportError:
        print("Библиотека colorama не подключена")

    

def log ( text, log_level):
    # Функция для распределения вывода сообщений
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    levels = {
        1: (TColor.GREEN, 1),   # info
        2: (TColor.CYAN, 2),    # info2
        3: (TColor.MAGENTA, 3), # warning
        4: (TColor.RED, 0),     # error (всегда выводится)
        5: (TColor.GRAY, 5),    # debug1
    }
    
    color, min_level = levels.get(log_level, (TColor.YELLO, 0))
    
    # пишем в файл
    if generate_log_file == 1:
        if  log_level <= log_informativeness or log_level == 4:
            log_file.writelines(f"{timestamp} {text}\n")
            
    # выводим в консоль
    if log_level == 4 or log_informativeness >= min_level:
        print(f"{color}[{timestamp}]{TColor.ENDC} {text}")    

            
def trim_log_file_tail(path, max_bytes=1024*1024):
    # Функция обрезки лог файла если размер превышает max_bytes
    if not os.path.exists(path):
        return

    size = os.path.getsize(path)
    if size <= max_bytes:
        log(f"Обрезка файла лога не нужна. Размер файла {size} <= {max_bytes}",5)
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

def path_is_valid_for_os(path: str) -> bool:
    # Функция валидации пути для фильтрации неправильных строк в имени файла в конфиге
    if os.name == "posix":  # Linux / macOS
        # Windows-путь выглядит как C:\ или D:\ , проверяем это
        if re.match(r"^[A-Za-z]:\\", path):
            return False
        # Обратные слеши для Linux — подозрительны
        if "\\" in path:
            return False
        return True

    elif os.name == "nt":  # Windows
        invalid_chars = r'<>:"|?*'
        return not any(ch in path for ch in invalid_chars)

    return True

        
def close_log():
    if generate_log_file == 1:
        trim_log_file_tail(log_file_path, max_bytes=log_file_size*1024)
        log_file.writelines("\n"*5)
        log_file.close()


# Инициализация лог файла        
script_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(f"{script_root_dir}{os.sep}nod32ms.conf",encoding='utf-8')        # Считываем файл конфигурации nod32ms.conf

generate_log_file = int(config.get('LOG','generate_log_file'))
log_informativeness = int(config.get('LOG','log_informativeness'))
log_file_size = int(config.get('LOG','log_file_size'))
default_log_file_path = f"{script_root_dir}{os.sep}pynod-mirror-tool.log"     # Дефолтное расположение лога в папке со скриптом
log_file_path = str(config.get('LOG','log_file_path', fallback=default_log_file_path))
    
if generate_log_file == 1:
    # Проверки валидности пути лог файла
    if log_file_path == "":
        log_file_path = default_log_file_path
            
    if not path_is_valid_for_os(log_file_path):
        # не валидный путь лог файла, пишем в папку со скриптом
        text_msg = f"ВНИМАНИЕ! Формат пути файла лога не валидный для данной ОС {log_file_path}"
        print(f"{TColor.RED}{'-'*len(text_msg)}\n{text_msg}")
        print(f"Лог будем писать в {default_log_file_path}\n{'-'*len(text_msg)}{TColor.ENDC}")
        log_file_path = default_log_file_path

    if not os.path.isabs(log_file_path):
        # в конфиге путь не абсолютный, лог будет записан относительно пути скрипта    
        log_file_path = f"{script_root_dir}{os.sep}{log_file_path}"        

    try:
        # Создаем папки в пути если не существуют
        target_path = os.path.dirname(log_file_path)
        if target_path and not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
            
        log_file = open(log_file_path, "a", encoding='utf-8')        
    except Exception as e:
        # Если какая-то ошибка создания лог файла по пути из конфига,
        # пробуем писать лог в папку со скриптом
        text_msg =f"Ошибка создания лог файла по пути из конфига:"
        print(f"{TColor.RED}{'-'*len(text_msg)}\n{text_msg}\n{e}\n{'-'*len(text_msg)}\n{TColor.ENDC}")
        log_file_path = default_log_file_path
        
        try:            
            log_file = open(log_file_path, "a", encoding='utf-8')
            
        except Exception as f:
            # Похоже файл лога записать не получится, попробуем работать без лога
            text_msg = f"Похоже файл лога записать не получится, попробуем работать без лога:"
            print(f"{TColor.RED}{'-'*len(text_msg)}\n{text_msg}\n{f}\n{'-'*len(text_msg)}\n{TColor.ENDC}")
            generate_log_file = 0
            
    if generate_log_file != 0:
        
        text_msg = f"Пишем лог файл в папку с именем {log_file_path}"
        
        print(f"{TColor.GREEN}{'-'*len(text_msg)}\n{text_msg}\n{'-'*len(text_msg)}\n{TColor.ENDC}")
        
            #f"{text_msg}\n"
            #f"{line}{TColor.ENDC}"
            #)
        
        # Обрезаем файл лога
        trim_log_file_tail(log_file_path, max_bytes=log_file_size*1024)
        log_file.write(f"\n{'='*40} НОВАЯ СЕССИЯ  {'='*40} \n")
    