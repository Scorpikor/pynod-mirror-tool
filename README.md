# pynod-mirror-tool
python mirror tool  to create local mirror nod32 antivirus bases
ВНИМАНИЕ! Скрипт ключи не ищет. Его задача подключиться к серверу зеркала баз NOD32, скачать базы и разложить
по папкам, чтоб другие антивирусы смогли обновиться.

24.10.2024 Update
+ Добавлен функционал повторных попыток скачивания файла при проблемах соединения
+ Добавлена проверка необходимости скачивания файла.
+ Добавлена отчистка от старых файлов и папок, которые не нужны в текущей версии баз
+ Добавлено визуальное оформление вывода
+ Добавлен параметр информативности вывода, который можно поменять в файле /inc/log.py = log_informativeness
+ Теперь базы каждой версии лежат в отдельной папке с соответствующим именем
