import asyncio
from telegram import Bot

TELEGRAM_TOKEN = '7713206299:AAG1IujWcXQPMKvgaIeoHKmsHRGWU02-zb8'
WEBHOOK_URL = 'https://masteryodo.pythonanywhere.com/webhook'

async def set_webhook():
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.set_webhook(WEBHOOK_URL)
    print('Webhook успешно установлен.')
    await bot.close()  # Корректное закрытие бота

if __name__ == '__main__':
    asyncio.run(set_webhook())
