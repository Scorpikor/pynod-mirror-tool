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
from collections import deque
import threading


#from http import HTTPStatus
from requests.exceptions import HTTPError
# ==========================
from concurrent.futures import ThreadPoolExecutor, as_completed
from ping3 import ping,verbose_ping

    
def tools_download_file(session,download_dict):
    # Скачиваем файл, возвращаем размер файла в байтах
    downloaded_size = 0
    error = None                                                            # Маркер ошибки скачивания
    error_text = ""                                                         # Текст ошибки
    mirror_connect_retries = ['mirror_connect_retries']                     # кол-во попыток перекачать файл
    log("tools.py:tools_download_file",5)
    headers = {"User-Agent": download_dict['user_agent']}                   # Добавляем в хэдеры юзерагент
    url = download_dict['download_url']                                     # URL для скачивания файла
    bar_color = download_dict['colour'] 
    log("tools.py:tools_download_file: Download URL: " + str(url),5)
    path_to_save = download_dict['save_path']                               # Путь для сохранения файла
    log(f"tools.py:tools_download_file: SAVE PATH: {path_to_save}",5)  
    server_timeout = download_dict['server_timeout']                        # Таймаут операций подключения
    # Добавляем авторизацию 
    if download_dict['server_user'] and download_dict['server_password']:
        auth1 = (download_dict['server_user'], download_dict['server_password'])        
    else:
        auth1 = None
                
    # Проверяем, указан ли в словаре размер скачиваемого файла
    if download_dict['file_size']:
        total_size = download_dict['file_size']
        log(f"tools.py:tools_download_file: {url} Размер файла берем из update.ver: {total_size}",5)
        leave = False
    else:
        leave = True    # для того, чтоб было видно скачивание update.ver
    
    # Проверка существования файла и его размера у нас если размер указан в словаре
    if os.path.exists(path_to_save) and download_dict['file_size']:
        local_file_size = os.path.getsize(path_to_save)  # Размер локального файла
        if local_file_size == total_size:
            log(str(download_dict['text']) + " " + str(path_to_save) + " Файл уже существует " + str(local_file_size) + " байт.", 5)
            return error, error_text,0, path_to_save # Возвращаем 0(байт) т.к. файл мы не скачивали с сервера

            
    # Если файл не существует или его размер отличается, выполняем загрузку
    try:
        response = session.get(url, headers=headers, auth=auth1, stream=True, timeout=server_timeout)
        response.raise_for_status()
        
    except Exception as e:
        error = 1
        error_text = str(e)
        # =======================================================
        log(f"tools.py:tools_download_file: Ошибка соеднинения с сервером. Файл {url}",5)        
        log (str(e),5)
        return error, error_text, downloaded_size, path_to_save
        #sys.exit(1)
        
    log(f"tools.py:tools_download_file: Запрос к серверу: {str(response.request.headers)}",5)
    log(f"tools.py:tools_download_file: Ответ от сервера: {str(response.headers)}",5)
    
    total_size = int(response.headers.get('content-length', 0))    
                    
    os.makedirs(os.path.dirname(path_to_save), exist_ok=True)
    with open(path_to_save, "wb") as file, tqdm(
        desc=download_dict['text'],
        total=total_size,
        unit='B',
        unit_scale=True,
        ascii=True,
        colour = bar_color,
        leave=leave,
        unit_divisor=1024,
    ) as bar:
            try:
            
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    bar.update(len(data))
            except Exception as e:
                error = 1
                error_text = str(e)
                log (str(e),5)
                return error, error_text, downloaded_size, path_to_save
                
    downloaded_size = os.path.getsize(path_to_save)
    
    if downloaded_size != total_size:
        error = 1
        error_text =  f"Размер скачанного файла ({downloaded_size} байт) не совпадает с ожидаемым ({total_size} байт)"
        log(error_text, 3) 
    
    
    return error, error_text, downloaded_size, path_to_save

    
def move_cursor_to(x, y):
    # Функция для перемещения курсора в указанное место
    print(f"\033[{y};{x}H", end='')


def clear_line():
    # Функция для очистки строки
    print("\033[K", end='')    
        
    
def pbar_colour(number):
    # выбираем цвет текста прогрессбара файла в зависимоссти от текущей попытки скачать файл
    colors =[
    'green',
    'yellow',
    'red'
    ]
    if number > 2:
        number = 2
    if number < 0:
        number = 0
    return colors[number]

def download_files_concurrently(download_dict, files_to_download):
    # Параллельная загрузка файлов
    new_files =[]                                   # Список новых файлов с путями, сохраненных в хранилище 
    error = None                                    # Статус скачивания файлов общий
    error_text = ""                                 # Текст ошибки
    stop_downloading = False                        # Флаг остановки загрузки
    retries_all = 0                                 # счетчик кол-ва попыток перекачать файл из-за каких-либо проблем
    os_separator = download_dict['os_separator']
    version = download_dict['version']
    desc = f"[{version}] Общий прогресс"            # сообщение индикатора выполнения
    path_fix = download_dict['path_fix']            # корневая папка для хранения файлов баз в корне папки web сервера

    # Прогресс-бар
    pbar = tqdm(total=len(files_to_download), desc=desc, colour='cyan', ascii=True, unit="file")

    def prepare_and_download(session, base_url, file_path, file_size, os_separator, version, retry_count):
        # Подготовка словаря для скачивания каждого файла базы и вызов tools_download_file
            
        if not file_path.startswith("/"):               # фиксим путь, когда в update.ver файл не начинается с "/"
            file_path = f"{path_fix}/{file_path}"
            
        file_url = f"{base_url}{file_path}"                                                 # url для скачивания файла
        save_path = f"{download_dict['save_path']}{file_path.replace('/',os_separator)}"    # путь для сохранения файла   
        
        download_file_dict = {
            'download_url': file_url,
            'colour': pbar_colour(retry_count),
            'save_path': save_path,
            'user_agent': download_dict['user_agent'],
            'server_user': download_dict['server_user'],
            'server_password': download_dict['server_password'],
            'server_timeout': download_dict['server_timeout'],
            'file_size': file_size,
            'text': f"[{version}] [{retry_count}] {file_path.split('/')[-1]}"  # Имя файла для отображения в tqdm
        }
        return tools_download_file(session, download_file_dict)

    # Максимальное количество попыток
    max_retries = download_dict['mirror_connect_retries']     # кол-во попыток скачать файл
    max_workers = download_dict['max_workers']      # кол-во потоков скачивания
    retry_count = {}                                # Счётчик попыток скачивания для каждого файла
    downloaded_size_version_result = 0              # Общий размер скачанных данных
    downloaded_files_version_result = 0             # Количество успешно скачанных файлов      
    # =========================================================================
    
    # Очередь задач
    task_queue = deque([(file_path, file_size) for file_path, file_size in files_to_download])

    with ThreadPoolExecutor(max_workers= max_workers) as executor:
        with requests.Session() as session:
            futures = {}  # Активные задачи

            # Пока есть задачи в очереди или активные задачи
            while task_queue or futures:
                # Заполняем пул задач
                while task_queue : #and len(futures) < len(files_to_download)//2:
                    if not stop_downloading:
                        file_path, file_size = task_queue.popleft()  # Берём задачу из начала очереди
                        future = executor.submit(
                            prepare_and_download, session, download_dict['mirror_server'], file_path, file_size, os_separator, version, retry_count.get(file_path, 0)
                        )
                        futures[future] = (file_path, file_size)
                    else:
                        break

                # Обрабатываем завершённые задачи
                for future in as_completed(futures):
                    
                    file_path, file_size = futures.pop(future)

                    # Выполнение функции tools_download_file
                    err, err_text, downloaded_size, path_to_save = future.result()

                    if err is None:  # Если файл скачан успешно
                        new_files.append(path_to_save)  # добавляем путь к сохраненному в хранилище файлу
                        if downloaded_size != 0:
                            downloaded_size_version_result += downloaded_size
                            downloaded_files_version_result += 1
                    else:
                        # Если ошибка, увеличиваем счётчик попыток
                        retries_all += 1
                        retry_count[file_path] = retry_count.get(file_path, 0) + 1
                        log(f"tools.prepare_and_download : Ошибка скачивания файла: {file_path}. Добавляем в очередь для повторной попытки.  ",5)
                        if retry_count[file_path] <= max_retries and not stop_downloading:
                            # Добавляем задачу в начало очереди
                            task_queue.appendleft((file_path, file_size))
                        else:
                            # Лимит попыток достигнут, останавливаем загрузку
                            log(f"tools.prepare_and_download : Ошибка скачивания файла: {file_path}. Кол-во поыток скачать файл закончилось...",5)
                            error = 1
                            error_text += f"Ошибка: {file_path.split('/')[-1]} пропущен после {max_retries} попыток. {err_text}\n"
                            stop_downloading = True  # Устанавливаем флаг остановки
                            #executor.shutdown(wait=False)
                            #futures.clear()
                            #task_queue.clear()
                            #cancel_event.set()  # Устанавливаем событие для остановки всех задач
                            break  # Прерываем цикл обработки задач

                    # Обновляем прогресс-бар
                    pbar.update(1)

    pbar.close()

    # Возвращаем:
    # error                             - Ошибку, если была = 1 или не было = None
    # error_text                        - Текст ошибки
    # downloaded_size_version_result    - Размер скачанных файлов
    # downloaded_files_version_result   - Количество скачанных файлов
    # retries_all                       - общее кол-во попыток перекачать файл
    # new_files                         - список сохраненных файлов в хранилище
    return error, error_text, downloaded_size_version_result, downloaded_files_version_result, retries_all, new_files
    
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
    
def elements_to_delete(files_new, files_all):
    # Из files_all убираем files_new, чтоб осталось то, что надо удалить
    log("tools.py:unique_elements",5)
    return [target for target in files_all if target not in files_new]
    
    
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
    creation_time = os.path.getmtime(file_path)
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
        sys.exit(1)
        
        
def init_filepath_fix(osseparator,filepath):
    # фиксим путь в соответствии с ОС
    return filepath.replace('/', osseparator)
    
def error_text_fix(text):
    # Удаляем потенциально опасные символы, из-за которых может не отправиться сообщение в телеграм
    text = text.translate(str.maketrans({"<": "", ">": "", "'": "", '"': ""}))
    return text
    
    