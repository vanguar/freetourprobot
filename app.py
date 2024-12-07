from flask import Flask, request
from telegram import Update
from bot import create_application
from config import WEBHOOK_URL, WEBHOOK_URL_PATH

# Создание Flask приложения
app = Flask(__name__)

# Инициализация бота
telegram_app = create_application()

# Установка webhook при старте
with app.app_context():
    try:
        telegram_app.bot.set_webhook(url=WEBHOOK_URL)
        print(f"Webhook установлен на {WEBHOOK_URL}")
    except Exception as e:
        print(f"Ошибка при установке webhook: {e}")

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    """Обработчик webhook-запросов от Telegram."""
    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        telegram_app.process_update(update)
        return 'OK', 200
    except Exception as e:
        print(f"Ошибка при обработке update: {e}")
        return 'Error', 500