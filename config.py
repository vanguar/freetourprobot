# config.py

import os
from dotenv import load_dotenv

# Загрузка переменных из .env с указанием пути
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Получаем токен бота из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Настройки вебхука
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', 'masteryodo.pythonanywhere.com')
WEBHOOK_URL_PATH = os.getenv('WEBHOOK_URL_PATH', '/webhook')
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_URL_PATH}"

# Проверка обязательных переменных
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не установлен! Проверьте файл .env и config.py.")
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL не установлен! Проверьте файл .env и config.py.")
