import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, WSGIHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация Flask-приложения
app = Flask(__name__)

# Инициализация Telegram бота
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '7713206299:AAG1IujWcXQPMKvgaIeoHKmsHRGWU02-zb8')
WEBHOOK_URL = 'https://masteryodo.pythonanywhere.com/webhook'

# Создание приложения telegram бота
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я ваш бот.')

# Добавление обработчиков
start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

# Обработчик ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

application.add_error_handler(error_handler)

# Настройка WSGI-обработчика для Telegram бота
application.wsgi_app = WSGIHandler()

# Маршрут для вебхука
@app.route('/webhook', methods=['POST'])
def webhook():
    return application.handle(request.environ, start_response)

if __name__ == '__main__':
    # Установка вебхука при запуске (опционально, если вы уже установили его)
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.set_webhook(WEBHOOK_URL)
    # Запуск Flask-приложения
    app.run()
