# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import configparser
import time
import os
from inc.class_tools import *

def log ( text, log_level):
    
    log_informativeness = 2 # может принимать значения от 1 до 5. 1 - минимум информации, 5 - для отладки
   
    if log_level == 1:          # info
        if log_informativeness >= 1:
            text_line = TColor.GREEN + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text)
            print(text_line)
    if log_level == 2:          # info2
        if log_informativeness >= 2:
            text_line = TColor.CYAN + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text) 
            print(text_line)
    if log_level == 3:          # warning
        if log_informativeness >= 3:
            text_line = TColor.MAGENTA + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text)
            print(text_line)
    if log_level == 4:          # error
        text_line = TColor.RED + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text)
        print(text_line)
    if log_level == 5:          # debug
        if log_informativeness >= 5:
            text_line = TColor.YELLO + "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "] " + TColor.ENDC + str(text)
            print(text_line)
