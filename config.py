# config.py

import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# Получение токена и настроек вебхука
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_URL_PATH = os.getenv('WEBHOOK_URL_PATH')
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_URL_PATH}"

# Проверка, что все переменные установлены
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не установлен! Проверьте файл .env.")
if not WEBHOOK_HOST or not WEBHOOK_URL_PATH:
    raise ValueError("WEBHOOK_HOST или WEBHOOK_URL_PATH не установлены! Проверьте файл .env.")
