# pynod-mirror-tool - Dockerized
 ![Version](https://img.shields.io/badge/version-20250509-gold)
 [![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg)](https://badge.fury.io/py/tensorflow)
 ![Last commit](https://img.shields.io/github/last-commit/Scorpikor/pynod-mirror-tool/main?cacheSeconds=0)
[![Opened issues](https://img.shields.io/github/issues/Scorpikor/pynod-mirror-tool?color=darkred)](https://github.com/rzc0d3r/ESET-KeyGen/issues?cacheSeconds=0)
[![Closed issues](https://img.shields.io/github/issues-closed/Scorpikor/pynod-mirror-tool?color=darkgreen&cacheSeconds=0)](https://github.com/rzc0d3r/ESET-KeyGen/issues?q=is%3Aissue+is%3Aclosed)
![License](https://img.shields.io/github/license/Scorpikor/pynod-mirror-tool)

python-mirror-tool is a Python script for creating a mirror of ESET NOD32 antivirus databases

pynod-mirror-tool  - скрипт, написанный на Рython для создания зеркала баз антивируса ESET NOD32. Поддерживаются операционные системы Windows, Linux, FreeBSD и возможен запуск в Docker, для работы требуется Python 3.x версии и NGINX для раздачи баз антивирусам.

# Установка:
1) cd pynod-mirror-tool
2) pip3 install -r requiments.txt
3) Редактируем файл nod32ms.conf под себя
4) запуск скачивания баз python3 update.py
5) Для раздачи баз антивирусам рекомендуется использовать NGINX, конфиг которого лежит тут же (папка nginx-configs, подбираем под свою версию nginx)


Быстрый запуск в docker: docker compose up -d

ВНИМАНИЕ! Скрипт ключи не ищет. Его задача подключиться к серверу зеркала баз NOD32 официальному (если у вас есть действующий логин и пароль) и не официальному, скачать базы и разложить
по папкам, после чего через NGINX раздать антивирусам или другим зеркалам.

# 19.06.2025 Update
+ добавлена возможность логирования в текстовый файл, соответствующие настройки добавились в nod32ms.conf раздел [LOG] 
+ настройка информативности вывода в терминал и в текстовый лог из log.py перенесена в конфиг nod32ms.conf раздел [LOG]

# 11.06.2025 Update
+ файлы патча PROTOSCAN для баз v3 заменены на версию 1454

# 10.05.2025 Update
+ добавлена секция в nod32ms.conf [PATCH] и параметр protoscan_v3_patch, который включает применение патча PROTOSCAN для баз v3 и включает файлы версии 1400.4
+ исправлены баги с чисткой старых файлов
+ изменено поведение скрипта при ошибке 401 (ошибка авторизации). Теперь скрипт больше не пытается закачать остальные файлы базы
+ устранены мелкие косяки и конечно же добавлены новые :) 

# 19.03.2025 Update
+ В конфиге в разделе [TELEGRAM] добавлен параметр text для вывода текста или напоминания в сообщении telegram
+ Исправлен алгоритм закачки файла и проверки его размера с поддержкой сжатия
+ update.ver теперь отчищается от лишних строк, мешающих антивирусам нормально обновляться с зеркала, созданного скриптом

# 3.03.2025 Update
+ Вернул генерацию html
+ устранены мелкие глюки

# 24.02.2025 Update
+ Добавлена поддержка Windows
+ Добавлена многопоточная закачка баз
+ Исправлены некоторые баги обновления прошлой версии
+ Теперь update.ver не меняется, что предотвращает "накопление путей" в этом файле при обновлении с зеркал, созданных таким же скриптом
+ Добавлена отправка отчетов в Telegram

Внимание!  Файл конфигурации nod32ms.conf и файл nginx изменились и для своего сервера необходимо настроить их под себя
- Временно не работает генерация html
  
# 21.11.2024 Update
+ В конфигурационном файле добавлен переключатель для обновлений с официальных серверов ESET или с зеркал, (параметр official_servers_update в nod32ms.conf),
  который переключает файлы переменных окружения (init.py для режима обновления с зеркала) и  (init_official.py для обновления с официальных серверов ESET)
+ В режиме обновления с официальных серверов ESET проверяется сервер с меньшим пингом и обновление уже происходит с него.
+ Добавлена генерация веб страницы, которую можно посмотреть в браузере, так же можно создать отдельную таблицу.
+ Добавлены некоторые незначительные улучшения.

# 24.10.2024 Update
+ Добавлен функционал повторных попыток скачивания файла при проблемах соединения
+ Добавлена проверка необходимости скачивания файла.
+ Добавлена отчистка от старых файлов и папок, которые не нужны в текущей версии баз
+ Добавлено визуальное оформление вывода
+ Добавлен параметр информативности вывода, который можно поменять в файле /inc/log.py = log_informativeness
+ Теперь базы каждой версии лежат в отдельной папке с соответствующим именем и структура папок нового скрипта не совместима с предыдущей  версией, поэтому, обновляя скрипт на новый, отчистите вручную хранилище файлов баз

Пример работы скрипта:
![image](https://github.com/user-attachments/assets/fb27198b-6a60-435f-b1a9-076e99aaca23)

