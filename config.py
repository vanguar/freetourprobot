import os

# Загружайте TELEGRAM_TOKEN из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Убедитесь, что токен успешно загружается
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не установлен! Проверьте файл .env и config.py.")
