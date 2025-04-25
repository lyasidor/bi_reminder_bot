import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Токен Telegram бота
BOT_API_KEY = os.getenv("BOT_API_KEY", "7777339725:AAHd7AkbFBYRrcUl4wwGdbDsKvBo0b0FMGk")

# Параметры для работы с базой данных (если понадобится)
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///tasks.db")