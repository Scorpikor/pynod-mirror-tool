# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

from inc.log import *
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
        
    if ver == 'v10':
        # Не работает
        return {
        'fix': '',
        'upd' : 'eset_upd/v10/dll/update.ver',
        'dll' : 'eset_upd/v10/dll/update.ver',
        'name' : 'ESET NOD32 Ver. 10'
        }
    
    if ver == 'v12':
        return {
        'fix': '/dll',
        'upd' : 'eset_upd/v12/dll/update.ver',
        'dll' : 'eset_upd/v12/dll/update.ver',
        'name' : 'ESET NOD32 Ver. 12'
        }
    
    if ver == 'v14':
        return {
        'fix': '/dll',
        'upd' : 'eset_upd/v14/dll/update.ver',
        'dll' : 'eset_upd/v14/dll/update.ver',
        'name' : 'ESET NOD32 Ver. 14'
        }

    if ver == 'v15':
        return {
        'fix': '/dll',
        'upd' : 'eset_upd/v15/dll/update.ver',
        'dll' : 'eset_upd/v15/dll/update.ver',
        'name' : 'ESET NOD32 Ver. 15'
        }

    if ver == 'v16':
        return {
        'fix': '/dll',
        'upd' : 'eset_upd/v16/dll/update.ver',
        'dll' : 'eset_upd/v16/dll/update.ver',
        'name' : 'ESET NOD32 Ver. 16'
        }

    if ver == 'v18':
        return {
        'fix': '/dll',
        'upd' : 'eset_upd/consumer/windows/full/dll/update.ver',
        'dll' : 'eset_upd/v18/dll/update.ver',
        'name' : 'ESET NOD32 Ver. 17 - 18'
        }

    if ver == 'ep6':
        return {
        'fix': '/dll',                                  # Добавочный путь, нужен когда в update.ver пути без каталогов 
        'upd' : 'eset_upd/ep6.6/update.ver',            # Путь, по которому сам ep6 запрашивает update.ver с сервера обновлений
        'dll' : 'eset_upd/ep6/dll/update.ver',          # Путь, по которому будет лежать update.ver у нас на зеркале
        'name' : 'ESET NOD32 Endpoint Ver. 6'           # Описание
        }   
    
    if ver == 'ep8':
        return {
        'fix': '/dll',                                  # Добавочный путь
        'upd' : 'eset_upd/ep8/dll/update.ver',          # Путь, по которому сам ep8 запрашивает update.ver с сервера обновлений
        'dll' : 'eset_upd/ep8/dll/update.ver',          # Путь, по которому будет лежать update.ver у нас на зеркале
        'name' : 'ESET NOD32 Endpoint Ver. 8'           # Описание
        }   

    if ver == 'ep9':
        return {
        'fix': '/dll',                                  # Добавочный путь
        'upd' : 'dll/update.ver',                       # Путь, по которому сам ep9 запрашивает update.ver с сервера обновлений
        'dll' : 'eset_upd/ep9/dll/update.ver',          # Путь, по которому будет лежать update.ver у нас на зеркале
        'name' : 'ESET NOD32 Endpoint Ver. 9'           # Описание
        }    

    if ver == 'ep10':
        return {
        'fix': '/dll',                                  # Добавочный путь
        'upd' : 'dll/update.ver',                       # Путь, по которому сам ep10 запрашивает update.ver с сервера обновлений
        'dll' : 'eset_upd/ep10/dll/update.ver',         # Путь, по которому будет лежать update.ver у нас на зеркале
        'name' : 'ESET NOD32 Endpoint Ver. 9'           # Описание
        }   
    
    if ver == 'ep11':
        return {
        'fix': '/dll',                                  # Добавочный путь
        'upd' : 'dll/update.ver',                       # Путь, по которому сам ep11 запрашивает update.ver с сервера обновлений
        'dll' : 'eset_upd/ep11/dll/update.ver',         # Путь, по которому будет лежать update.ver у нас на зеркале
        'name' : 'ESET NOD32 Endpoint Ver. 11'          # Описание
        }

    if ver == 'ep12':
        return {
        'fix': '/dll',                                 # Добавочный путь
        'upd' : 'dll/update.ver',                      # Путь, по которому сам ep12 запрашивает update.ver с сервера обновлений
        'dll' : 'eset_upd/ep12/dll/update.ver',        # Путь, по которому будет лежать update.ver у нас на зеркале
        'name' : 'ESET NOD32 Endpoint Ver. 12'         # Описание
        }

    else:
        log("Неопределенная версия " + str(ver) + " в init.py",4)
        sys.exit(1)
