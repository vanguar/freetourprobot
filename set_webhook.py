# set_webhook.py

import asyncio
from bot import application
from config import WEBHOOK_URL

async def set_wb():
    await application.bot.set_webhook(WEBHOOK_URL)
    print("Вебхук установлен успешно.")

if __name__ == '__main__':
    asyncio.run(set_wb())
