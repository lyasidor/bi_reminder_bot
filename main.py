import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.ext import ConversationHandler

from handlers import get_conv_handler, list_tasks

load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")

if not token:
    raise ValueError("Токен не найден в .env файле!")

def main():
    app = ApplicationBuilder().token(token).build()

    # Добавляем обработчики
    app.add_handler(get_conv_handler())
    app.add_handler(CommandHandler("tasks", list_tasks))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()