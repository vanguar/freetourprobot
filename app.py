# app.py

import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application
from config import TELEGRAM_TOKEN, WEBHOOK_URL, WEBHOOK_URL_PATH
from bot import setup_bot

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Создание Flask приложения
app = Flask(__name__)

# Создание приложения бота
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Настройка бота
setup_bot(application)

# Маршрут для вебхука
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
async def webhook():
    # Получаем обновление от Telegram
    update = Update.de_json(await request.get_json(force=True), application.bot)
    # Обрабатываем обновление
    await application.process_update(update)
    return 'OK', 200

# Запуск приложения не требуется, так как оно будет запускаться через WSGI
