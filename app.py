# app.py

import sys
import os
import json
import asyncio
from telegram import Update
from telegram.ext import Dispatcher
from bot import application, setup_bot
from config import WEBHOOK_URL_PATH

# Инициализация бота и добавление обработчиков
setup_bot()

async def handle_update(update_json):
    dispatcher = application.dispatcher
    update = Update.de_json(update_json, application.bot)
    await dispatcher.process_update(update)

def application(environ, start_response):
    if environ['PATH_INFO'] == WEBHOOK_URL_PATH and environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size)
        update_json = json.loads(request_body.decode('utf-8'))

        # Создаём новый цикл событий для обработки обновления
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(handle_update(update_json))
        loop.close()

        # Возвращаем ответ Telegram
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']
    else:
        # Возвращаем 404 для других маршрутов
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']
