from telegram import Bot
from dotenv import load_dotenv
import os

# Загрузка переменных из .env с указанием пути
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = f"https://{os.getenv('WEBHOOK_HOST')}{os.getenv('WEBHOOK_URL_PATH')}"

def set_webhook():
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.set_webhook(WEBHOOK_URL)
    print('Webhook успешно установлен.')

if __name__ == '__main__':
    set_webhook()
