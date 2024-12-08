from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Инициализация бота при старте
telegram_app = create_application()
telegram_app.initialize()  # Важно: инициализируем приложение

def run_async(coro):
    """Выполняет асинхронную функцию в синхронном контексте"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            update = Update.de_json(request.get_json(force=True), telegram_app.bot)
            logger.info("Получен webhook запрос")
            logger.info(f"Получен update: {update}")
            
            # Синхронно запускаем асинхронную обработку
            run_async(telegram_app.process_update(update))
            return 'ok'
        except Exception as e:
            logger.error(f"Ошибка при обработке update: {e}")
            return 'Error processing update', 500
    return 'ok'

@app.route('/')
def index():
    return 'Bot is running'