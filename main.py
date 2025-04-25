from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from handlers import task_name, task_date, time, task_comment

# Определяем состояния для ConversationHandler
TASK_NAME, TASK_DATE, TASK_TIME, TASK_COMMENT = range(4)

def main():
    # Создаем приложение с токеном
    application = Application.builder().token('7777339725:AAHd7AkbFBYRrcUl4wwGdbDsKvBo0b0FMGk').build()

    # Создаем обработчик для команд
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

    # Добавляем обработчик в приложение
    application.add_handler(conversation_handler)

    # Запускаем бота в режиме polling
    application.run_polling()

if __name__ == '__main__':
    main()
