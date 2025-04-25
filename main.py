from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from handlers import start, add_task, show_tasks, delete_task
from buttons import start_buttons, back_button, task_buttons

def main():
    # Замените на свой токен
    TOKEN = '7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o'
    updater = Application(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчики команд
    dp.add_handler(CommandHandler("start", start))

    # Обработчики кнопок
    dp.add_handler(CallbackQueryHandler(add_task, pattern='^add_task$'))
    dp.add_handler(CallbackQueryHandler(show_tasks, pattern='^show_tasks$'))
    dp.add_handler(CallbackQueryHandler(delete_task, pattern='^delete_task_'))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
