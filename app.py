from flask import Flask, request, Response
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio
from telegram.ext import Application
from contextlib import asynccontextmanager
import sys

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Создание Flask приложения
app = Flask(__name__)

# Глобальные переменные
telegram_app = None
event_loop = None

@asynccontextmanager
async def bot_context():
    """Контекстный менеджер для корректной инициализации и закрытия бота."""
    global telegram_app
    if telegram_app is None:
        telegram_app = create_application()
        await telegram_app.initialize()
        await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook установлен на {WEBHOOK_URL}")
    try:
        yield telegram_app
    finally:
        pass  # Не закрываем приложение после каждого запроса

def run_async(coroutine):
    """Запуск асинхронного кода в синхронном контексте."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик webhook-запросов от Telegram."""
    if request.method == "POST":
        try:
            async def process_update():
                async with bot_context() as bot:
                    update = Update.de_json(request.get_json(force=True), bot.bot)
                    logger.info(f"Получен update: {update}")
                    await bot.process_update(update)

            run_async(process_update())
            return Response('OK', status=200)
        except Exception as e:
            logger.error(f"Ошибка при обработке webhook: {e}", exc_info=True)
            return Response(f'Error: {str(e)}', status=500)
    return Response(status=403)

@app.route('/')
def index():
    return 'Bot is running'

# Инициализация бота при старте
try:
    run_async(bot_context().__aenter__())
    logger.info("Bot initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize bot: {e}", exc_info=True)