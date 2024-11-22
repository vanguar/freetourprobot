# config.py

from dotenv import load_dotenv
load_dotenv()
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получаем токен бота из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Настройки вебхука
WEBHOOK_HOST = 'masteryodo.pythonanywhere.com'  # Замените на ваш действительный домен
WEBHOOK_PORT = 443  # Порт для вебхуков
WEBHOOK_URL_PATH = '/webhook'  # Путь к вебхуку
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_URL_PATH}"

# Локальный адрес и порт для встроенного веб-сервера (не используются на PythonAnywhere)
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
