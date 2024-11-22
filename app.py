# app.py

from flask import Flask, request
from bot import application, setup_bot
from config import WEBHOOK_URL, WEBHOOK_URL_PATH, FLASK_HOST, FLASK_PORT
import asyncio

app = Flask(__name__)

# Инициализируем бота и добавляем обработчики
setup_bot()

# Маршрут для обработки вебхуков
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.method == "POST":
        update = request.get_json(force=True)
        # Передаём обновление боту для обработки
        asyncio.run(application.process_update(update))
        return 'OK'
    else:
        return 'Method Not Allowed', 405

# Маршрут для проверки работы Flask
@app.route('/')
def home():
    return "Hello, World!"

# Функция для установки вебхука (выполняется один раз)
def set_webhook():
    application.bot.set_webhook(WEBHOOK_URL)

if __name__ == '__main__':
    # Устанавливаем вебхук (не требуется на PythonAnywhere, лучше сделать вручную через консоль)
    set_webhook()
    
    # Запускаем Flask-приложение (не требуется на PythonAnywhere)
    app.run(host=FLASK_HOST, port=FLASK_PORT)
