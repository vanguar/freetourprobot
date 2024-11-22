# config.py

from dotenv import load_dotenv
load_dotenv()
import os

# Получаем токен бота из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Настройки вебхука
WEBHOOK_HOST = 'masteryodo.pythonanywhere.com'  # Ваш домен на PythonAnywhere
WEBHOOK_PORT = 443  # Обычно порт 443 для HTTPS
WEBHOOK_URL_PATH = '/webhook'  # Путь к вебхуку
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_URL_PATH}"

# Эти параметры не нужны для WSGI-приложения и могут быть удалены или оставлены без использования
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000

