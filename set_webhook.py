import asyncio
from bot import application
from config import WEBHOOK_URL

async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)
    print("Webhook successfully set.")

if __name__ == "__main__":
    asyncio.run(set_webhook())
