# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import requests
from tqdm import tqdm
import os
import shutil
import sys
from inc.log import *

def tools_download_file(session,download_dict):
    # Скачиваем файл, возвращаем размер файла в байтах
    log("tools.py:tools_download_file",5)
    headers = {"User-Agent": download_dict['user_agent']}
    url = download_dict['download_url']
    log("tools.py:tools_download_file: Download URL: " + str(url),5)
    
    # Добавляем авторизацию 
    if download_dict['server_user'] and download_dict['server_password']:
        auth1 = (download_dict['server_user'], download_dict['server_password'])
        
    else:
        auth1 = None
        
    path_to_save = download_dict['save_path']
    log("tools.py:tools_download_file: SAVE PATH: " + str(path_to_save),5)
    server_timeout = download_dict['server_timeout']
    
    if download_dict['file_size']:
        total_size = download_dict['file_size']
        log("tools.py:tools_download_file: Размер файла берем из update.ver: " + str(total_size),5)
    else:    
        try:
            response = session.get(url, headers=headers, auth=auth1, stream=True, timeout=server_timeout)
            log("tools.py:tools_download_file: Запрос к серверу: ",5)
            log(str(response.request.headers),5)
            log("tools.py:tools_download_file: Ответ от сервера:",5)
            log(str(response.headers),5)
            total_size = int(response.headers.get('content-length', 0))
            log("tools.py:tools_download_file: Размер файла берем с сервера: " + str(total_size),5)
            if response.status_code == 401:                
                log("tools.py:tools_download_file: " + str(url) + " 401 Сервер требует авторизацию! Необходимо проверить правильность указанных данных авторизации в файле конфигурации!",4)
                log("tools.py:tools_download_file: Завершение работы скрипта!",4)
                sys.exit(1)
            if response.status_code == 403:                
                log("tools.py:tools_download_file: " + str(url) + " 403 Доступ запрещен! Необходимо проверить правильность URL для скачивания!",4)
                log("tools.py:tools_download_file: Завершение работы скрипта!",4)
                sys.exit(1)
            if response.status_code == 404:                
                log("tools.py:tools_download_file: " + str(url) + " 404 Файл на сервере не найден! Необходимо проверить правильность URL для скачивания!",4)
                log("tools.py:tools_download_file: Завершение работы скрипта!",4)
                sys.exit(1)
        except Exception as e:
            log("tools.py:tools_download_file: Произошла ошибка:",4)
            log (e,4)
            log("tools.py:tools_download_file: Завершение работы скрипта!",4)
            sys.exit(1)
    
    # Проверка существования файла и его размера
    if os.path.exists(path_to_save):
        local_file_size = os.path.getsize(path_to_save)  # Размер локального файла
        if local_file_size == total_size:
            log(str(path_to_save) + " Файл уже существует и его размер совпадает " + str(local_file_size) + " байт. Скачивание не требуется.", 3)
            return 0 #local_file_size
            
    # Если файл не существует или его размер отличается, выполняем загрузку
    try:
        response = session.get(url, headers=headers, auth=auth1, stream=True, timeout=server_timeout)
        if response.status_code == 404:                
                log(str(url) + " Файл на сервере не найден! Необходимо проверить правильность URL для скачивания!",4)
                log("tools.py:tools_download_file: Завершение работы скрипта!",4)
                sys.exit(1)
    except Exception as e:
        log("Произошла ошибка при скачивании: " + str(e),4)
        log("tools.py:tools_download_file: Завершение работы скрипта!",4)
        sys.exit(1)
    
    os.makedirs(os.path.dirname(path_to_save), exist_ok=True)
    with open(path_to_save, "wb") as file, tqdm(
        desc=download_dict['text'],
        total=total_size,
        unit='B',
        unit_scale=True,
        ascii=True,
        colour ='green',       
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))
    downloaded_size = os.path.getsize(path_to_save)
    return downloaded_size
    
def move_file(source_path, destination_path):
    # Перемещаем файл
    log("tools.py:move_file",5)
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    shutil.move(source_path, destination_path)
    log("Файл перемещён в " + str(destination_path),5)
    
def modify_update_ver(updatever_file_path, prefix):
    # Функция модифицирует в update.ver параметр file, добавляя префикс
    log("tools.py:modify_update_ver",5)
    log("UPDATE.VER prefix: " + str(prefix),5)
    with open(updatever_file_path, 'r') as file:
        lines = file.readlines()
        
    new_lines = []
    for line in lines:
        if line.startswith("file="):
            parts = line.split('=', 1)
            if not parts[1].startswith("/"):
                parts[1] = '/'+ parts[1]
            modified_line = parts[0] + "=" + prefix + parts[1]
            new_lines.append(modified_line)
        else:
            new_lines.append(line)
            
    with open(updatever_file_path, 'w') as file:
        file.writelines(new_lines)

def folder_size(folder_path):
    # Функция возвращает размер папки в байтах
    log("tools.py:folder_size",5)
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            # Проверяем, что это файл (на случай символических ссылок)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size
    
def sizeof_fmt(num):
    # Функция переводит байты в удобный формат
    log("tools.py:sizeof_fmt",5)
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')
    
def convert_seconds(seconds):
    # Переводим секунды в удобный формат
    log("tools.py:convert_seconds",5)
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60  # Здесь остаются секунды, включая дробные
    
    result = []
    if days > 0:
        result.append(f"{days} дн.")
    if hours > 0:
        result.append(f"{hours} ч.")
    if minutes > 0:
        result.append(f"{minutes} мин.")
    
    # Используем точность до двух знаков для секунд
    if seconds > 0 or not result:
        result.append(f"{seconds:.2f} сек.")
    
    return " ".join(result)
    
def list_files_and_folders(directory):
    # Возвращаем список файлов и папок в директории
    log("tools.py:list_files_and_folders",5)
    file_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
           file_list.append(os.path.join(dirpath, filename))
    return file_list
    
def unique_elements(list1, list2):
    # Из двух списков оставляем только уникальные не повторяющиеся значения
    log("tools.py:unique_elements",5)
    return list(set(list1) ^ set(list2))
    
def delete_files(list):
    # Удаляем файлы согласно списка
    log("tools.py:delete_files",5)
    for file in list:
        os.remove(file)
    log("tools.py:delete_files: Старые файлы удалены",5)
    
def remove_empty_folders(directory):
    # Удаляем пустые папки
    log("tools.py:remove_empty_folders",5)
    count = 0
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        # Если директория пустая (нет файлов и подкаталогов)
        if not dirnames and not filenames:
            count += 1 
            log("tools.py:remove_empty_folders: Удаление пустой папки: "+ str(dirpath),5)
            os.rmdir(dirpath)
    log("Кол-во пустых папок удалено: " + str(count),2)
