from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio
import nest_asyncio

# Применяем nest_asyncio для вложенных event loops
nest_asyncio.apply()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
telegram_app = None

def get_application():
    """Инициализация приложения"""
    global telegram_app
    if telegram_app is None:
        telegram_app = create_application()
        asyncio.run(telegram_app.bot.set_webhook(url=WEBHOOK_URL))
    return telegram_app

# Инициализация при старте
telegram_app = get_application()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            update = Update.de_json(request.get_json(), telegram_app.bot)
            logger.info(f"Получен webhook запрос")
            logger.info(f"Получен update: {update}")
            
            # Создаем новый event loop для каждого запроса
            asyncio.run(telegram_app.process_update(update))
            
            return 'ok'
        except Exception as e:
            logger.error(f"Ошибка при обработке update: {e}")
            return 'Error processing update', 500
    return 'ok'

@app.route('/')
def index():
    return 'Bot is running'