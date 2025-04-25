from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from handlers import start, button_handler

def main():
    """Запуск бота"""
    updater = Updater("7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o", use_context=True)
    dispatcher = updater.dispatcher

    # Добавляем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота
    updater.start_polling()

    # Бот будет работать до тех пор, пока не будет остановлен вручную
    updater.idle()

if __name__ == '__main__':
    main()