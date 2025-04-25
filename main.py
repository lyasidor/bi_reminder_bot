from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from handlers import start, handle_button_click, handle_text
from states import ADD_TASK, CHOOSE_DATE, ENTER_TIME, ENTER_COMMENT, LIST_TASKS
from keyboard import start_keyboard, back_button
import logging

# Настройки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    updater = Updater('7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o', use_context=True)
    dp = updater.dispatcher

    # Главный разговор
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start, pattern='^start$')],
        states={
            ADD_TASK: [MessageHandler(Filters.text & ~Filters.command, handle_text)],
            CHOOSE_DATE: [CallbackQueryHandler(handle_button_click, pattern='^date_')],
            ENTER_TIME: [MessageHandler(Filters.text & ~Filters.command, handle_text)],
            ENTER_COMMENT: [MessageHandler(Filters.text & ~Filters.command, handle_text)],
            LIST_TASKS: [CallbackQueryHandler(handle_button_click, pattern='^task_')]
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(handle_button_click))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()