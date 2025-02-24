# Этот файл является частью проекта PyNOD-Mirror-Tool
# актуальную версию которого можно скачть по адресу:
# https://github.com/Scorpikor/pynod-mirror-tool

import requests
from inc.log import *

def send_msg(text, token, chat_id):
    
    
    send_message_url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
    'chat_id': chat_id,
    'text': text,
    'parse_mode': 'HTML'
    
    }
    
    response = requests.post(send_message_url, data=payload)
    log(f"Telegram text: {text}",3)
    log(f"Telegram response: {response.json()}",3)
 
 
