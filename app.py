from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio
from telegram.ext import Application
from functools import partial
import nest_asyncio

# Инициализируем nest_asyncio для решения проблем с event loop
nest_asyncio.apply()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
telegram_app = None

def setup_application():
    """Настройка приложения с сохранением event loop"""
    global telegram_app
    if telegram_app is None:
        telegram_app = create_application()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(telegram_app.initialize())
            loop.run_until_complete(telegram_app.bot.set_webhook(url=WEBHOOK_URL))
            logger.info(f"Webhook установлен на {WEBHOOK_URL}")
        except Exception as e:
            logger.error(f"Ошибка при инициализации: {e}")
    return telegram_app

# Инициализируем бот при старте
telegram_app = setup_application()

def run_async(coroutine):
    """Вспомогательная функция для запуска корутин"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик webhook-запросов от Telegram."""
    try:
        logger.info("Получен webhook запрос")
        
        if telegram_app is None:
            logger.error("Приложение не инициализировано")
            return 'Error: Application not initialized', 500
            
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logger.info(f"Получен update: {update}")
        
        run_async(telegram_app.process_update(update))
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Ошибка при обработке update: {e}", exc_info=True)
        return 'Error', 500

@app.route('/')
def index():
    return 'Bot is running'