# -*- coding: utf-8 -*-
# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool


import platform
import requests
from tqdm import tqdm
import os
import shutil
import sys
import datetime
from inc.log import *
# ==========================
from concurrent.futures import ThreadPoolExecutor, as_completed
from ping3 import ping,verbose_ping


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
        except Exception as e:
            log("tools.py:tools_download_file: Ошибка соеднинения с сервером. Сервер жив?:",4)
            log (str(e),4)
            log("tools.py:tools_download_file: Завершение работы скрипта!",4)
            sys.exit(1)
                   
        log("tools.py:tools_download_file: Запрос к серверу: ",5)
        log(str(response.request.headers),5)
        log("tools.py:tools_download_file: Ответ от сервера:",5)
        log(str(response.headers),5)
        total_size = int(response.headers.get('content-length', 0))
        log("tools.py:tools_download_file: Размер файла берем с сервера: " + str(total_size),5)
        if response.status_code != 200:
        
            if response.status_code == 401:                
                log("tools.py:tools_download_file: " + str(url) + " 401 Сервер требует авторизацию! Необходимо проверить правильность указанных данных авторизации в файле конфигурации!",4)                
            if response.status_code == 403:                
                log("tools.py:tools_download_file: " + str(url) + " 403 Доступ запрещен! Необходимо проверить правильность URL для скачивания!",4)                
            if response.status_code == 404:                
                log("tools.py:tools_download_file: " + str(url) + " 404 Файл на сервере не найден! Необходимо проверить правильность URL для скачивания!",4)                
            else:
                log("tools.py:tools_download_file: " + str(url) + " " + str(response.status_code) + " Ошибка",4)
                
            log("tools.py:tools_download_file: Завершение работы скрипта!",4)
            sys.exit(1)
    
    # Проверка существования файла и его размера у нас
    if os.path.exists(path_to_save):
        local_file_size = os.path.getsize(path_to_save)  # Размер локального файла
        if local_file_size == total_size:
            log(str(download_dict['text']) + " " + str(path_to_save) + " Файл уже существует " + str(local_file_size) + " байт.", 3)
            return 0 # Возвращаем 0(байт) т.к. файл мы не скачивали с сервера
            
    # Если файл не существует или его размер отличается, выполняем загрузку
    try:
        response = session.get(url, headers=headers, auth=auth1, stream=True, timeout=server_timeout)
        if response.status_code == 404:                
                log(str(url) + " Файл на сервере не найден! Необходимо проверить правильность URL для скачивания! Возможно, на сервере обновилась база.",4)
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

def file_creation_datetime(file_path):
    # Возвращает дату создания файла
    creation_time = os.path.getctime(file_path)
    creation_date = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
    return creation_date

def ping_server(server, attempts=3):
    # Пингует сервер и возвращает среднее время отклика
    times = []
    for _ in range(attempts):
        result = ping(server, timeout=2, unit='ms')  # Вызываем ping с таймаутом
        if result != None and result != 0 and result != False:  # Если ответ не пустой
            times.append(result)  # Добавляем результат в список
            
    log(str(server)+ " " + str(times),5)
    if times:
        avg_time = sum(times)/len(times)
        return server, avg_time
    else:
        return server, None  # Если сервер не ответил ни разу
        
def choosing_the_best_server(oficial_servers):
    # Выбираем лучший официальный сервер для обновления
    log("Выбираем лучший официальный сервер для обновлений...",1)
    results = []
    with ThreadPoolExecutor(max_workers=len(oficial_servers)) as executor:
        future_to_server = {executor.submit(ping_server, server): server for server in oficial_servers}
        for future in as_completed(future_to_server):
            server = future_to_server[future]
            try:
                server, avg_time = future.result()
                if avg_time != None:
                    results.append((server, avg_time))
            except Exception as exc:
                print(f"tools.py:choosing_the_best_server: {server} вызвал исключение: {exc}")
                sys.exit(1)
                
    # Выбираем сервер
    if len(results)== 0:
        log("tools.py:choosing_the_best_server: Нет живых серверов для обновления",4)
        log("tools.py:choosing_the_best_server: Завершение работы скрипта",4)
        sys.exit(1)
    elif len(results) == 1:
        server, avg_time = results[0]
        log("tools.py:choosing_the_best_server: Только один живой сервер " + str(server) + " " + str(avg_time),5)
        return server, avg_time
    else:
        best_server = None
        best_time = 10000
        for server, avg_time in results:
            if avg_time is not None:
                if avg_time < best_time :
                    best_server = server
                    best_time = avg_time
        
        return best_server, best_time
        
def os_dir_separator():
    os_platform = platform.system()
    if os_platform == "Linux":
        log("tools.py:os_dir_separator: Используем платформу Linux",2)
        return os_platform, "/"
    elif os_platform == "Windows":
        log("tools.py:os_dir_separator: Используем платформу Windows",2)
        return os_platform, "\\"
    else:
        log("tools.py:choosing_the_best_server: Платформа, на которой запущен скрипт, не тестировалась!",4)
        log("tools.py:choosing_the_best_server: Если есть большая необходимость запустить скрипт именно на вашей платворме, обратитесь к автору скрипта.",4)
        log("tools.py:choosing_the_best_server: Завершение работы скрипта",4)
    