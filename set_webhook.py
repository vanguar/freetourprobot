import asyncio
from telegram import Bot
from config import TELEGRAM_TOKEN, WEBHOOK_URL

async def set_webhook():
    """Устанавливает webhook для бота."""
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.set_webhook(url=WEBHOOK_URL)
    print('Webhook успешно установлен.')

if __name__ == '__main__':
    asyncio.run(set_webhook())