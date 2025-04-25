from telegram.ext import Application
from handlers import start_handler, help_handler, add_task_handler, list_tasks_handler, message_handler

def main():
    # Вставьте свой токен
    application = Application.builder().token("7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o").build()

    # Добавляем обработчики
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(add_task_handler)
    application.add_handler(list_tasks_handler)
    application.add_handler(message_handler)

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
