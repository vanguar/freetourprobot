# app.py

from flask import Flask, request
from bot import application
from config import WEBHOOK_URL_PATH, WEBHOOK_URL
import asyncio

app = Flask(__name__)

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.method == "POST":
        update = request.get_json(force=True)
        # Передаём обновление боту для обработки
        asyncio.run_coroutine_threadsafe(application.process_update(update), asyncio.get_event_loop())
        return 'OK'
    else:
        return 'Method Not Allowed', 405

@app.route('/')
def home():
    return "Hello, World!"
