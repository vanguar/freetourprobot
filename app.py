from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio
import nest_asyncio

# Применяем nest_asyncio
nest_asyncio.apply()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
telegram_app = None

def create_app():
    """Создание и настройка приложения"""
    global telegram_app
    if telegram_app is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        telegram_app = create_application()
        try:
            loop.run_until_complete(telegram_app.initialize())
            loop.run_until_complete(telegram_app.bot.set_webhook(url=WEBHOOK_URL))
            logger.info(f"Webhook установлен на {WEBHOOK_URL}")
        finally:
            loop.close()
    return telegram_app

# Инициализация при старте
telegram_app = create_app()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logger.info(f"Получен update: {update}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(telegram_app.process_update(update))
        finally:
            loop.close()
            
        return 'OK', 200
    except Exception as e:
        logger.error(f"Ошибка при обработке update: {e}")
        return 'Error', 500

@app.route('/')
def index():
    return 'Bot is running'