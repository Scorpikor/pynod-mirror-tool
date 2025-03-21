# pynod-mirror-tool - Dockerized

python mirror tool  to create local mirror nod32 antivirus bases

Быстрый запуск: docker compose up -d

ВНИМАНИЕ! Скрипт ключи не ищет. Его задача подключиться к серверу зеркала баз NOD32, скачать базы и разложить
по папкам, чтоб другие антивирусы смогли обновиться.

19.03.2025 Update
+ В конфиге в разделе [TELEGRAM] добавлен параметр text для вывода текста или напоминания в сообщении telegram
+ Исправлен алгоритм закачки файла и проверки его размера с поддержкой сжатия
+ update.ver теперь отчищается от лишних строк, мешающих антивирусам нормально обновляться с зеркала, созданного скриптом

3.03.2025 Update
+ Вернул генерацию html
+ устранены мелкие глюки

24.02.2025 Update
+ Добавлена поддержка Windows
+ Добавлена многопоточная закачка баз
+ Исправлены некоторые баги обновления прошлой версии
+ Теперь update.ver не меняется, что предотвращает "накопление путей" в этом файле при обновлении с зеркал, созданных таким же скриптом
+ Добавлена отправка отчетов в Telegram

Внимание!  Файл конфигурации nod32ms.conf и файл nginx изменились и для своего сервера необходимо настроить их под себя
- Временно не работает генерация html
  
21.11.2024 Update
+ В конфигурационном файле добавлен переключатель для обновлений с официальных серверов ESET или с зеркал, (параметр official_servers_update в nod32ms.conf),
  который переключает файлы переменных окружения (init.py для режима обновления с зеркала) и  (init_official.py для обновления с официальных серверов ESET)
+ В режиме обновления с официальных серверов ESET проверяется сервер с меньшим пингом и обновление уже происходит с него.
+ Добавлена генерация веб страницы, которую можно посмотреть в браузере, так же можно создать отдельную таблицу.
+ Добавлены некоторые незначительные улучшения.

24.10.2024 Update
+ Добавлен функционал повторных попыток скачивания файла при проблемах соединения
+ Добавлена проверка необходимости скачивания файла.
+ Добавлена отчистка от старых файлов и папок, которые не нужны в текущей версии баз
+ Добавлено визуальное оформление вывода
+ Добавлен параметр информативности вывода, который можно поменять в файле /inc/log.py = log_informativeness
+ Теперь базы каждой версии лежат в отдельной папке с соответствующим именем и структура папок нового скрипта не совместима с предыдущей  версией, поэтому, обновляя скрипт на новый, отчистите вручную хранилище файлов баз

Пример работы скрипта:
![image](https://github.com/user-attachments/assets/c7269384-2c12-4fbd-bc4a-78dd3c65c184)
