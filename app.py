from flask import Flask, request
from bot import application, setup_bot
from config import WEBHOOK_URL, WEBHOOK_URL_PATH
import asyncio

app = Flask(__name__)

# Инициализируйте бота
setup_bot()

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = request.get_json(force=True)
        # Используйте application для обработки
        asyncio.run(application.process_update(update))
        return 'OK'
    else:
        return 'Method Not Allowed', 405

@app.route('/')
def home():
    return "Hello, World!"
