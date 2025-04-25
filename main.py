# main.py
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from handlers import start, handle_button_click, handle_text
from states import ADD_TASK, CHOOSE_DATE, ENTER_TIME, ENTER_COMMENT, LIST_TASKS
from keyboard import start_keyboard, back_button
import logging

# Настройки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Создаем экземпляр приложения
    application = Application.builder().token('7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o').build()

    # Главный разговор
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start, pattern='^start$')],
        states={
            ADD_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)],
            CHOOSE_DATE: [CallbackQueryHandler(handle_button_click, pattern='^date_')],
            ENTER_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)],
            ENTER_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)],
            LIST_TASKS: [CallbackQueryHandler(handle_button_click, pattern='^task_')]
        },
        fallbacks=[],
    )

    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_button_click))

    # Запускаем бота (асинхронно)
    application.run_polling()

# Если код запускается напрямую
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())  # Убираем этот вызов