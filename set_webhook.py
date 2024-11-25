# set_webhook.py

import os
from dotenv import load_dotenv
import asyncio

# Определяем путь к директории проекта
project_folder = os.path.expanduser('/home/MasterYodo/freetourprobot')
dotenv_path = os.path.join(project_folder, '.env')

# Загружаем переменные окружения из файла .env
load_dotenv(dotenv_path)

# Теперь импортируем bot и config
from bot import application
from config import WEBHOOK_URL

async def set_wb():
    await application.bot.set_webhook(WEBHOOK_URL)
    print("Вебхук установлен успешно.")

if __name__ == '__main__':
    asyncio.run(set_wb())
