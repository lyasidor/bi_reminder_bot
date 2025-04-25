from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from handlers import start, add_task, show_tasks, handle_task_selection
from buttons import main_keyboard, task_keyboard, task_details_keyboard
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Создаем объект Application (новый интерфейс)
    application = Application.builder().token("7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o").build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Обработчики кнопок
    application.add_handler(CallbackQueryHandler(add_task, pattern="^add_task$"))
    application.add_handler(CallbackQueryHandler(show_tasks, pattern="^show_tasks$"))
    application.add_handler(CallbackQueryHandler(handle_task_selection, pattern="^task_"))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()