import os

# Настройки базы данных
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///tasks.db")

# Токен вашего бота (не забудьте заменить на свой)
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN", "7777339725:AAHd7AkbFBYRrcUl4wwGdbDsKvBo0b0FMGk")
