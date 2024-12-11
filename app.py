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
    return event_loop

def init_telegram():
    """Инициализация Telegram бота"""
    global telegram_app
    if telegram_app is None:
        logger.info("Начало инициализации telegram_app")
        loop = get_event_loop()
        telegram_app = create_application()
        
        try:
            # Инициализируем приложение
            loop.run_until_complete(telegram_app.initialize())
            # Устанавливаем webhook
            loop.run_until_complete(telegram_app.bot.set_webhook(url=WEBHOOK_URL))
            logger.info(f"Webhook успешно установлен на {WEBHOOK_URL}")
        except Exception as e:
            logger.error(f"Ошибка при инициализации: {e}")

# Инициализируем бота при старте
init_telegram()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик webhook-запросов от Telegram."""
    if telegram_app is None:
        init_telegram()
        
    try:
        logger.info("Получен webhook запрос")
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logger.info(f"Получен update: {update}")
        
        loop = get_event_loop()
        loop.run_until_complete(telegram_app.process_update(update))
        return 'OK', 200
    except Exception as e:
        logger.error(f"Ошибка в webhook: {str(e)}")
        return 'Error', 500

@app.route('/')
def index():
    return 'Bot is running'