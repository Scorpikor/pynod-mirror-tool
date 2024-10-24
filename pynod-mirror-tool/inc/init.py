# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool


import sys

def init(ver):
   
    if ver == 'v3':
        return {
        'fix': '',
        'upd' : 'update.ver',
        'dll' : 'eset_upd/v3/dll/update.ver',
        'name' : 'ESET NOD32 Ver. 3-4, 6-8'
        }
    
    if ver == 'v5':
        return {
        'fix': '',
        'upd' : 'update.ver',
        'dll' : 'eset_upd/v5/dll/update.ver',
        'name' : 'ESET NOD32 Ver. 5'
        }
    
    if ver == 'ep11':
        return {
        'fix': '/dll',                                  # Добавочный путь
        'upd' : 'dll/update.ver',                       # Путь, по которому сам ep11 запрашивает update.ver с сервера обновлений
        'dll' : 'eset_upd/ep11/dll/update.ver',         # Путь, по которому будет лежать update.ver у нас на зеркале
        'name' : 'ESET NOD32 Endpoint Ver. 11'          # Описание
        }

    else:
        print ("Неопределенная версия", ver, "в init.py")
        sys.exit(1)
