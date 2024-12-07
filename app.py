from flask import Flask, request
from telegram import Update
from bot import application, setup_bot
from config import WEBHOOK_URL, WEBHOOK_URL_PATH

# Создание Flask приложения
app = Flask(__name__)

# Инициализация бота
setup_bot()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик webhook-запросов от Telegram."""
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.process_update(update)
        return 'OK', 200
    except Exception as e:
        print(f"Ошибка при обработке update: {e}")
        return 'Error', 500

# Установка webhook при запуске
@app.before_first_request
def setup_webhook():
    """Установка webhook для бота."""
    try:
        application.bot.set_webhook(url=WEBHOOK_URL)
        print(f"Webhook установлен на {WEBHOOK_URL}")
    except Exception as e:
        print(f"Ошибка при установке webhook: {e}")