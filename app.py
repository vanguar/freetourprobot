# app.py

from bot import application, setup_bot
from config import WEBHOOK_URL, WEBHOOK_URL_PATH, FLASK_HOST, FLASK_PORT

def main():
    # Инициализируем бота и добавляем обработчики
    setup_bot()

    # Запускаем приложение с вебхуком
    application.run_webhook(
        listen=FLASK_HOST,
        port=FLASK_PORT,
        url_path=WEBHOOK_URL_PATH,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == '__main__':
    main()
