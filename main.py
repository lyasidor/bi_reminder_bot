from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from handlers import start, handle_button_click, handle_text, ADD_TASK, ENTER_TIME, ENTER_COMMENT

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ADD_TASK: [MessageHandler(filters.TEXT, handle_text)],
        ENTER_TIME: [MessageHandler(filters.TEXT, handle_text)],
        ENTER_COMMENT: [MessageHandler(filters.TEXT, handle_text)]
    },
    fallbacks=[CallbackQueryHandler(handle_button_click)]
)

async def main():
    application = Application.builder().token('7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o').build()
    application.add_handler(conv_handler)
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())