# -*- coding: utf-8 -*-
# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import configparser
import time
import os
import sys
import platform
from inc.class_tools import *

# Глобальные переменные
generate_log_file = 0
log_informativeness = 3
log_file_path = ""
log_file_size = 0
log_file = None

def log(text, log_level):
    """
    Логирование сообщений с различными уровнями важности
    """
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log_message = f"{timestamp} {text}"
    
    # Запись в файл
    if generate_log_file == 1 and log_file and (log_level <= log_informativeness or log_level == 4):
        try:
            log_file.write(f"{log_message}\n")
            log_file.flush()
        except Exception as e:
            print(f"{TColor.RED}[ОШИБКА ЗАПИСИ В ЛОГ] {e}{TColor.ENDC}")

    # Вывод в консоль
    colors = {
        1: TColor.GREEN,
        2: TColor.CYAN,
        3: TColor.MAGENTA,
        4: TColor.RED,
        5: TColor.GRAY
    }
    color = colors.get(log_level, TColor.WHITE)

    if log_level <= log_informativeness or log_level == 4:
        print(f"{color}{log_message}{TColor.ENDC}")

def trim_log_file_tail(filepath, max_bytes=1024*1024):
    try:
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            if file_size > max_bytes:
                with open(filepath, "rb") as f:
                    f.seek(-max_bytes // 2, os.SEEK_END)
                    tail = f.read()
                with open(filepath, "wb") as f:
                    f.write(tail)
                print(f"{TColor.YELLO}[LOG] Ротация лога выполнена.{TColor.ENDC}")
    except Exception as e:
        print(f"{TColor.RED}[ОШИБКА РОТАЦИИ] {e}{TColor.ENDC}")

def close_log():
    global log_file
    if log_file:
        try:
            log_file.close()
        except:
            pass

# =============================================================================
# ИНИЦИАЛИЗАЦИЯ (Умная обработка путей)
# =============================================================================
# Определяем абсолютный путь к папке, где лежит скрипт (не важно откуда запущен)
# Поднимаемся на уровень выше, так как log.py лежит в папка /inc/
script_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
conf_path = os.path.join(script_root_dir, "nod32ms.conf")

try:
    config.read(conf_path, encoding='utf-8')
    
    generate_log_file = int(config.get('LOG', 'generate_log_file', fallback=0))
    log_informativeness = int(config.get('LOG', 'log_informativeness', fallback=3))
    log_file_size = int(config.get('LOG', 'log_file_size', fallback=1024)) 
    
    # 1. Читаем то, что написано в конфиге
    raw_log_path = config.get('LOG', 'log_path', fallback="nod32mirror.log")
    
    # 2. Проверяем, абсолютный ли это путь
    # Если путь начинается с / (Linux) или C:\ (Windows), os.path.isabs вернет True
    if os.path.isabs(raw_log_path):
        target_log_path = raw_log_path
    else:
        # Если путь относительный (просто имя файла), приклеиваем его к папке скрипта
        target_log_path = os.path.join(script_root_dir, raw_log_path)
    
    if generate_log_file == 1:
        try:
            # Создаем папку для лога, если её нет (для полных путей)
            log_dir = os.path.dirname(target_log_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            log_file = open(target_log_path, "a", encoding='utf-8')
            log_file_path = target_log_path
            
            trim_log_file_tail(log_file_path, max_bytes=log_file_size*1024)
            log_file.write("\n" + "="*30 + " NEW SESSION " + "="*30 + "\n")

        except PermissionError:
            # Если нет прав писать по указанному пути, пишем рядом со скриптом (Fallback)
            fallback_path = os.path.join(script_root_dir, "nod32mirror.log")
            print(f"{TColor.RED}[WARNING] Нет прав на {target_log_path}. Лог: {fallback_path}{TColor.ENDC}")
            try:
                log_file = open(fallback_path, "a", encoding='utf-8')
                log_file_path = fallback_path
            except:
                generate_log_file = 0
        except Exception as e:
            print(f"Log init error: {e}")
            generate_log_file = 0

except Exception as e:
    print(f"Log Config Error: {e}")