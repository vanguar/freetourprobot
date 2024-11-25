import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация Telegram бота и приложения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN не установлен в переменных окружения.")
    exit(1)

bot = Bot(token=TELEGRAM_TOKEN)
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

# Маршрут для вебхука
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        # Асинхронная обработка обновления
        application.create_task(application.process_update(update))
        return 'ok', 200

if __name__ == '__main__':
    # Установка вебхука (опционально, если вы уже установили его ранее)
    bot.set_webhook('https://masteryodo.pythonanywhere.com/webhook')
    # Запуск Flask-приложения
    app.run()
