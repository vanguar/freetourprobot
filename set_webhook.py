# set_webhook.py

from telegram import Bot
from config import TELEGRAM_TOKEN, WEBHOOK_URL

def set_webhook():
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.set_webhook(url=WEBHOOK_URL)
    print('Webhook успешно установлен.')

if __name__ == '__main__':
    set_webhook()
