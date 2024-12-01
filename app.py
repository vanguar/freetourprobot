import threading
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder
import os
from bot import setup_bot  # Импортируйте вашу функцию настройки бота

# Получение переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL_PATH = os.getenv('WEBHOOK_URL_PATH')

# Проверка наличия необходимых переменных
if not TELEGRAM_TOKEN:
    logging.error("TELEGRAM_TOKEN не установлен в переменных окружения.")
    raise ValueError("TELEGRAM_TOKEN не установлен в переменных окружения.")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Создание Flask приложения
app = Flask(__name__)

# Создание приложения бота
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Настройка бота
setup_bot(application)

# Маршрут для вебхука
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    # Получаем обновление от Telegram
    update = Update.de_json(request.get_json(force=True), application.bot)
    # Помещаем обновление в очередь обновлений бота
    application.update_queue.put_nowait(update)
    return 'OK', 200

# Функция для запуска приложения бота в отдельном потоке
def run_application():
    # Запускаем приложение бота с собственным циклом событий
    application.run_polling()

# Запускаем приложение бота в отдельном потоке
threading.Thread(target=run_application, daemon=True).start()
