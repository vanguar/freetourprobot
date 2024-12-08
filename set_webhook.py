import asyncio
from telegram import Bot
from config import TELEGRAM_TOKEN, WEBHOOK_URL

async def set_webhook():
    """Устанавливает webhook для бота."""
    bot = Bot(token=TELEGRAM_TOKEN)
    # Сначала удалим старый webhook
    await bot.delete_webhook()
    # Установим новый webhook
    success = await bot.set_webhook(url=WEBHOOK_URL)
    if success:
        print('Webhook успешно установлен.')
    else:
        print('Ошибка при установке webhook.')
    # Проверим текущие настройки webhook
    webhook_info = await bot.get_webhook_info()
    print(f'Текущий webhook URL: {webhook_info.url}')

if __name__ == '__main__':
    asyncio.run(set_webhook())