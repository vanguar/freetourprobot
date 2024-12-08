from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
telegram_app = create_application()
executor = ThreadPoolExecutor(max_workers=1)

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

def process_update_in_thread(update_json):
    try:
        update = Update.de_json(update_json, telegram_app.bot)
        run_async(telegram_app.process_update(update))
        return True
    except Exception as e:
        logger.error(f"Ошибка при обработке update: {e}")
        return False

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            logger.info("Получен webhook запрос")
            update_json = request.get_json(force=True)
            logger.info(f"Получен update: {update_json}")
            
            # Запускаем обработку в отдельном потоке
            executor.submit(process_update_in_thread, update_json)
            return 'ok'
        except Exception as e:
            logger.error(f"Ошибка при обработке webhook запроса: {e}")
            return 'Error processing webhook', 500
    return 'ok'

@app.route('/')
def index():
    return 'Bot is running'

if __name__ == '__main__':
    app.run()