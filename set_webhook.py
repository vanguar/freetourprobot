import asyncio
from bot import application

async def set_wb():
    await application.bot.set_webhook('https://masteryodo.pythonanywhere.com/webhook')

if __name__ == '__main__':
    asyncio.run(set_wb())
