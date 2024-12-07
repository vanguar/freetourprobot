from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio
from telegram.ext import Application
from functools import partial

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
telegram_app = None

def init_webhook(application):
    """Инициализация webhook в синхронном контексте"""
    async def _init():
        await application.initialize()
        await application.bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook установлен на {WEBHOOK_URL}")
    
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(_init())
    finally:
        loop.close()

def get_application():
    """Получение или создание экземпляра приложения"""
    global telegram_app
    if telegram_app is None:
        telegram_app = create_application()
        init_webhook(telegram_app)
    return telegram_app

# Инициализируем бота 
telegram_app = get_application()

def process_update_sync(update, application):
    """Обработка update в синхронном контексте"""
    async def _process():
        await application.process_update(update)
    
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(_process())
    finally:
        loop.close()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик webhook-запросов от Telegram."""
    try:
        logger.info("Получен webhook запрос")
        
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logger.info(f"Получен update: {update}")
        
        process_update_sync(update, telegram_app)
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Ошибка при обработке update: {e}")
        return 'Error', 500

@app.route('/')
def index():
    return 'Bot is running'