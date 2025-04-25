from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler
from handlers import start, button_handler

def main():
    """Запуск бота"""
    application = Application.builder().token("YOUR_BOT_API_TOKEN").build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()