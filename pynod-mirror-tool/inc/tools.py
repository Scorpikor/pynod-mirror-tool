import requests
from tqdm import tqdm
import os
import shutil
import sys

def tools_download_file(session,download_dict):
    headers = {"User-Agent": download_dict['user_agent']}
    url = download_dict['download_url']
    #print("Download URL:", url)
    
    # Добавляем авторизацию на сервере 
    if download_dict['server_user'] and download_dict['server_password']:
        auth1 = (download_dict['server_user'], download_dict['server_password'])
        #print("Server User:", download_dict['server_user'])
        #print("Server Password:", download_dict['server_password'])
    else:
        auth1 = None
        #print ("Без авторизации")
        
    path_to_save = download_dict['save_path']
    server_timeout = download_dict['server_timeout']
    
    try:
        response = session.get(url, headers=headers, auth=auth1, stream=True, timeout=server_timeout)
        #print("Запрос к серверу:", response.request.headers)  
        #print("Ответ от сервера:", response.headers)
        total_size = int(response.headers.get('content-length', 0))
    except Exception as e:
        print("Произошла ошибка:", e)
        sys.exit(1)
        
    os.makedirs(os.path.dirname(path_to_save), exist_ok=True)
    with open(path_to_save, "wb") as file, tqdm(
        desc=url,
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
    #print(f"Размер скачанного файла: {downloaded_size} байт")
    return downloaded_size
    
def move_file(source_path, destination_path):
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    shutil.move(source_path, destination_path)
    print(f"Файл перемещён в {destination_path}")