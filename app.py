from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Создаем и инициализируем приложение при старте
telegram_app = create_application()
telegram_app.initialize()  # Инициализируем приложение
telegram_app.start()  # Запускаем приложение

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик вебхуков от Telegram."""
    if request.method == 'POST':
        try:
            update = Update.de_json(request.get_json(force=True), telegram_app.bot)
            logger.info("Получен webhook запрос")
            logger.info(f"Получен update: {update}")
            
            # Запускаем обработку обновления через TaskQueue
            telegram_app.update_queue.put(update)
            return 'ok'
        except Exception as e:
            logger.error(f"Ошибка при обработке update: {e}")
            return 'Error processing update', 500
    return 'ok'

@app.route('/')
def index():
    return 'Bot is running'

if __name__ == '__main__':
    app.run()