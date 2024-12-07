from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Создание Flask приложения
app = Flask(__name__)

# Инициализация бота
telegram_app = create_application()

# Инициализация приложения
async def initialize():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    logger.info(f"Webhook установлен на {WEBHOOK_URL}")

# Запуск инициализации в event loop
with app.app_context():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize())
    except Exception as e:
        logger.error(f"Ошибка при инициализации: {e}")

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик webhook-запросов от Telegram."""
    try:
        logger.info("Получен webhook запрос")
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logger.info(f"Получен update: {update}")
        
        # Создаём новый event loop для асинхронной обработки
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(telegram_app.process_update(update))
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Ошибка при обработке update: {e}")
        return 'Error', 500

@app.route('/')
def index():
    return 'Bot is running'