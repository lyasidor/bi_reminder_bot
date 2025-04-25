import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Токен Telegram бота
BOT_API_KEY = os.getenv("BOT_API_KEY")