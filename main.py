import asyncio
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from handlers import get_conv_handler, list_tasks_handler
from scheduler import scheduler

from config import BOT_TOKEN

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("tasks", list_tasks_handler))
    app.add_handler(get_conv_handler())

    scheduler.start()

    print("Бот запущен.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())