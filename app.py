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

# Глобальная переменная для приложения
telegram_app = None

def init_telegram():
    """Инициализация Telegram бота"""
    global telegram_app
    if telegram_app is None:
        telegram_app = create_application()
        
        # Создаём новый event loop для асинхронной инициализации
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Инициализируем приложение
            loop.run_until_complete(telegram_app.initialize())
            # Устанавливаем webhook
            loop.run_until_complete(telegram_app.bot.set_webhook(url=WEBHOOK_URL))
            logger.info(f"Webhook установлен на {WEBHOOK_URL}")
        except Exception as e:
            logger.error(f"Ошибка при инициализации: {e}")
        finally:
            loop.close()

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
        
        # Создаём новый event loop для асинхронной обработки
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