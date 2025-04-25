from telegram.ext import Application
from handlers import start, handle_button_click, handle_text, ADD_TASK, ENTER_TIME, ENTER_COMMENT, conv_handler

async def main():
    application = Application.builder().token('YOUR_BOT_TOKEN').build()
    application.add_handler(conv_handler)
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    # Запускаем main() напрямую через asyncio.run()
    asyncio.run(main())