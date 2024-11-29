# app.py

import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher
from dotenv import load_dotenv

from bot import dispatcher  # Импортируем dispatcher из bot.py

# Загрузка переменных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация бота
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN не установлен в переменных окружения.")
    exit(1)

bot = Bot(token=TELEGRAM_TOKEN)

# Маршрут для вебхука
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return 'ok', 200

if __name__ == '__main__':
    # Установка вебхука
    bot.set_webhook('https://masteryodo.pythonanywhere.com/webhook')
    # Запуск Flask-приложения
    app.run()
