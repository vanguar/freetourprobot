from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio
from telegram.ext import Application

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Создание Flask приложения
app = Flask(__name__)

# Глобальные переменные
telegram_app = None
event_loop = None

def get_event_loop():
    """Получение или создание event loop"""
    global event_loop
    try:
        event_loop = asyncio.get_event_loop()
    except RuntimeError:
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
    
    if event_loop.is_closed():
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
    
    return event_loop

async def init_app():
    """Асинхронная инициализация приложения"""
    global telegram_app
    if telegram_app is None:
        telegram_app = create_application()
        await telegram_app.initialize()
        await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook установлен на {WEBHOOK_URL}")
    return telegram_app

def ensure_app_initialized():
    """Убеждаемся, что приложение инициализировано"""
    global telegram_app
    if telegram_app is None:
        loop = get_event_loop()
        telegram_app = loop.run_until_complete(init_app())

# Инициализируем бота при старте
ensure_app_initialized()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик webhook-запросов от Telegram."""
    try:
        logger.info("Получен webhook запрос")
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logger.info(f"Получен update: {update}")
        
        loop = get_event_loop()
        # Добавляем дополнительную проверку и инициализацию
        if telegram_app is None or not telegram_app.running:
            loop.run_until_complete(init_app())
            
        loop.run_until_complete(telegram_app.process_update(update))
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Ошибка при обработке update: {e}")
        return 'Error', 500

@app.route('/')
def index():
    return 'Bot is running'