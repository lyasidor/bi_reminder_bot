from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from handlers import task_name, task_date, time, task_comment, show_tasks, delete_task, start
from database import add_task_to_db, get_tasks_from_db, delete_task_from_db
from keyboard import get_task_buttons, get_task_list_buttons

# Определяем состояния для ConversationHandler
TASK_NAME, TASK_DATE, TASK_TIME, TASK_COMMENT = range(4)

def main():
    application = Application.builder().token('7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o').build()

    # Обработчики
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_name)],
            TASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_date)],
            TASK_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, time)],
            TASK_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_comment)],
        },

        fallbacks=[],
    )

    application.add_handler(conversation_handler)
    application.add_handler(CallbackQueryHandler(show_tasks, pattern='^show_tasks$'))
    application.add_handler(CallbackQueryHandler(delete_task, pattern='^delete_task_'))

    application.run_polling()

if __name__ == '__main__':
    main()
