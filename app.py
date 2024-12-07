from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio
from telegram.ext import Application

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
telegram_app = None

def get_application():
    """Получение или создание экземпляра приложения"""
    global telegram_app
    if telegram_app is None:
        telegram_app = create_application()
        # Инициализируем приложение сразу при создании
        asyncio.run(telegram_app.initialize())
        asyncio.run(telegram_app.bot.set_webhook(url=WEBHOOK_URL))
        logger.info(f"Webhook установлен на {WEBHOOK_URL}")
    return telegram_app

# Инициализируем бота при старте
get_application()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
async def webhook():
    """Обработчик webhook-запросов от Telegram."""
    try:
        logger.info("Получен webhook запрос")
        application = get_application()
        
        update = Update.de_json(request.get_json(force=True), application.bot)
        logger.info(f"Получен update: {update}")
        
        # Создаем новый event loop для каждого запроса
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            await application.process_update(update)
        finally:
            loop.close()
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Ошибка при обработке update: {e}")
        return 'Error', 500

@app.route('/')
def index():
    return 'Bot is running'