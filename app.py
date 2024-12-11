from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import logging
import asyncio
from telegram.ext import Application
from pathlib import Path

# Создаем директорию для хранения данных, если её нет
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Создаем файл для хранения состояния бота, если его нет
persistence_path = data_dir / "bot_persistence"
if not persistence_path.exists():
    persistence_path.touch()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Создание Flask приложения
app = Flask(__name__)

# Глобальные переменные
telegram_app = None
event_loop = None

def get_event_loop():
    """Получение или создание event loop"""
    global event_loop
    try:
        event_loop = asyncio.get_event_loop()
    except RuntimeError:
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
    return event_loop

def init_telegram():
    """Инициализация Telegram бота"""
    global telegram_app
    if telegram_app is None:
        loop = get_event_loop()
        telegram_app = create_application()
        
        try:
            # Инициализируем приложение
            loop.run_until_complete(telegram_app.initialize())
            # Устанавливаем webhook
            loop.run_until_complete(telegram_app.bot.set_webhook(url=WEBHOOK_URL))
            logger.info(f"Webhook установлен на {WEBHOOK_URL}")
        except Exception as e:
            logger.error(f"Ошибка при инициализации: {e}")

# Инициализируем бота при старте
init_telegram()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик webhook-запросов от Telegram."""
    if telegram_app is None:
        logger.info("Инициализация приложения, так как telegram_app is None")
        init_telegram()
        
    try:
        logger.info("Получен webhook запрос")
        update_data = request.get_json(force=True)
        logger.info(f"Получены данные: {update_data}")
        
        update = Update.de_json(update_data, telegram_app.bot)
        logger.info(f"Преобразовано в Update: {update}")
        
        # Проверяем тип обновления
        if update.message and update.message.text == '/start':
            logger.info(f"Получена команда /start от пользователя {update.effective_user.id}")
            
        # Получаем event loop
        loop = get_event_loop()
        
        # Обрабатываем update
        try:
            loop.run_until_complete(telegram_app.process_update(update))
            logger.info("Update успешно обработан")
        except Exception as e:
            logger.error(f"Ошибка при обработке update: {str(e)}")
            raise
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Ошибка в webhook: {str(e)}")
        return 'Error', 500