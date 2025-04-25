from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from handlers import start, add_task, task_name, task_date, task_time, task_comment, show_tasks, task_details, delete_task

# Определение состояний для ConversationHandler
TASK_NAME, TASK_DATE, TASK_TIME, TASK_COMMENT = range(4)

# Инициализация приложения
def main():
    application = Application.builder().token('YOUR_BOT_TOKEN').build()

    # Команды
    application.add_handler(CommandHandler("start", start))

    # Обработчик разговоров
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_name)],  # Ввод названия задачи
            TASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_date)],  # Ввод даты
            TASK_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_time)],  # Ввод времени
            TASK_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_comment)],  # Ввод комментария
        },

        fallbacks=[],
    )

    # Кнопки для просмотра задач
    application.add_handler(CallbackQueryHandler(show_tasks, pattern='^show_tasks$'))
    application.add_handler(CallbackQueryHandler(task_details, pattern='^task_details_'))
    application.add_handler(CallbackQueryHandler(delete_task, pattern='^delete_task_'))

    application.add_handler(conversation_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()