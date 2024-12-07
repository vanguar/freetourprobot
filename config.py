import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# Настройки бота
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Настройки webhook
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', 'masteryodo.pythonanywhere.com')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 443))
WEBHOOK_URL_PATH = os.getenv('WEBHOOK_URL_PATH', '/webhook')
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_URL_PATH}"

# Flask настройки
FLASK_HOST = '0.0.0.0'
FLASK_PORT = int(os.getenv('FLASK_PORT', 8443))