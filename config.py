# config.py

import os
import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/tmp/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Получаем токен бота из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
logger.info(f"TELEGRAM_TOKEN: {TELEGRAM_TOKEN}")

# Настройки вебхука
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', 'masteryodo.pythonanywhere.com')  # Замените на ваш действительный домен
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '443'))  # Порт для вебхуков
WEBHOOK_URL_PATH = os.getenv('WEBHOOK_URL_PATH', '/webhook')  # Путь к вебхуку
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_URL_PATH}"
logger.info(f"WEBHOOK_URL: {WEBHOOK_URL}")

# Локальный адрес и порт для встроенного веб-сервера (не используются на PythonAnywhere)
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000

# Проверка обязательных переменных
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не установлен! Проверьте файл .env и config.py.")
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL не установлен! Проверьте файл .env и config.py.")
