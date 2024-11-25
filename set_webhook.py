# set_webhook.py

import os
from dotenv import load_dotenv
import asyncio

project_folder = os.path.expanduser('/home/MasterYodo/freetourprobot')
dotenv_path = os.path.join(project_folder, '.env')
load_dotenv(dotenv_path)

print(f"TELEGRAM_TOKEN: {os.getenv('TELEGRAM_TOKEN')}")
print(f"WEBHOOK_URL: {os.getenv('WEBHOOK_URL')}")
