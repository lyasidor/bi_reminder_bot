from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handlers import start, add_task, show_tasks, handle_task_selection
from buttons import main_keyboard, task_keyboard, task_details_keyboard
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Создаем объект Updater и получаем диспетчера для добавления обработчиков
    updater = Updater("YOUR_BOT_API_TOKEN", use_context=True)

    dp = updater.dispatcher

    # Обработчики команд
    dp.add_handler(CommandHandler("start", start))

    # Обработчики сообщений и кнопок
    dp.add_handler(CallbackQueryHandler(add_task, pattern="^add_task$"))
    dp.add_handler(CallbackQueryHandler(show_tasks, pattern="^show_tasks$"))
    dp.add_handler(CallbackQueryHandler(handle_task_selection, pattern="^task_"))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()