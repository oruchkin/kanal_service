from datetime import datetime

import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

from .credentials import google_creds
from .models import Order

TELEGRAM_BOT_TOKEN = "5418877358:AAF-rrQENPstmyF_rSCBMU3wmL49qaSRIi8"

def get_data_from_google_sheet() -> list:
    """
    Функция которая получает все данные из google sheet.
    """
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scopes=scopes)
    file = gspread.authorize(credentials)
    workbook = file.open('test')
    sheet = workbook.sheet1    
    data_from_sheet = sheet.get_all_values()
    return data_from_sheet


def get_dollar_value() -> float:
    """
    Функция для получения текущего курса доллара
    """
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    usd = data["Valute"]["USD"]["Value"]
    return float("{:.4f}".format(usd))

 
def send_notification_teleg(chat_id: str, text: str) -> bool:
    """
    Функция для отправки уведомлений (сообщений) в телеграмм
    """
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)
    return True


def check_delivery_time_expiration(order: Order) -> bool:
    """
    Функция которая проверят истекл ли срок для отправки,
    если уже истек - то отправляет уведомление в телеграмм админам.
    если True значит просрочено, если False значит не просрочено
    """
    if order.delivery_time < datetime.now():
        return True
    else:
        return False