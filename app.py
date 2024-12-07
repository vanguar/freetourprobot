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

def create_app():
    global telegram_app
    if telegram_app is None:
        telegram_app = create_application()
    return telegram_app

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
async def webhook():
    if request.method == 'POST':
        try:
            update = Update.de_json(request.get_json(), telegram_app.bot)
            logger.info(f"Получен webhook запрос")
            logger.info(f"Получен update: {update}")
            
            # Создаем новый event loop для каждого запроса
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                await telegram_app.process_update(update)
            finally:
                loop.close()
            
            return 'ok'
        except Exception as e:
            logger.error(f"Ошибка при обработке update: {e}")
            return 'Error processing update', 500
    return 'ok'

@app.route('/')
def index():
    return 'Bot is running'

# Инициализация при старте
telegram_app = create_app()