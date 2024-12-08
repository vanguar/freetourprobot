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
telegram_app = create_application()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logger.info(f"Получен webhook запрос")
        logger.info(f"Получен update: {update}")
        
        await telegram_app.process_update(update)
        return 'ok'
    except Exception as e:
        logger.error(f"Ошибка при обработке update: {e}")
        return 'Error processing update', 500

@app.route('/')
def index():
    return 'Bot is running'