from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from handlers import task_name, task_date, time, task_comment

# Определяем состояния для ConversationHandler
TASK_NAME, TASK_DATE, TASK_TIME, TASK_COMMENT = range(4)

def main():
    application = Application.builder().token('YOUR_TOKEN').build()

    # Обработчики
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', task_name)],

        states={
            TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_name)],  # Ввод названия задачи
            TASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_date)],  # Ввод даты
            TASK_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, time)],       # Ввод времени
            TASK_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_comment)],  # Ввод комментария
        },

        fallbacks=[],
    )

    application.add_handler(conversation_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
