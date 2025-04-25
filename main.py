import asyncio
import logging
from telegram.ext import Application, ContextTypes

from handlers import get_conv_handler, list_tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Токен бота
TOKEN = "YOUR_TOKEN_HERE"  # замените на ваш реальный токен

# Создание планировщика
scheduler = AsyncIOScheduler()

async def main():
    # Запуск планировщика
    scheduler.start()

    # Создание приложения Telegram
    application = Application.builder().token(TOKEN).build()

    # Добавление обработчиков
    application.add_handler(get_conv_handler())
    application.add_handler(list_tasks)

    # Сохраняем планировщик в context, если потребуется из обработчиков
    application.bot_data["scheduler"] = scheduler

    # Запуск бота
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())