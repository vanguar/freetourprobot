from dotenv import load_dotenv
load_dotenv()
import os

# Получаем токен бота из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Настройки вебхука
WEBHOOK_HOST = 'masteryodo.pythonanywhere.com'  # Например, '0bd9-46-96-9-41.ngrok-free.app'
WEBHOOK_PORT = 443  # Обычно порт 443 для вебхуков
WEBHOOK_URL_PATH = '/webhook'  # Путь к вебхуку
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_URL_PATH}"

# Локальный адрес и порт для встроенного веб-сервера
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
