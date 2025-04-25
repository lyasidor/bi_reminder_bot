from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from handlers import start, add_task, list_tasks, task_name, task_date, task_time, task_comment, cancel
from states import STATES

async def main():
    # Создание приложения с токеном бота
    application = Application.builder().token('YOUR_BOT_API_KEY').build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Обработчики задач
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STATES.TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_name)],
            STATES.TASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_date)],
            STATES.TASK_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_time)],
            STATES.TASK_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_comment)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(conversation_handler)

    # Запуск бота
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
