import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from handlers import start, handle_button_click, handle_text, ADD_TASK, ENTER_DATE, ENTER_TIME, ENTER_COMMENT, conv_handler

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Вставьте свой токен
    application = Application.builder().token('YOUR_BOT_TOKEN').build()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)  # Основной обработчик разговоров

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())