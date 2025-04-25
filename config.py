import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Токен Telegram бота
BOT_API_KEY = os.getenv("BOT_API_KEY")

# Параметры для работы с базой данных (если понадобится)
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///tasks.db")