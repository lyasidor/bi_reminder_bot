from telegram.ext import Application
from handlers import conv_handler

async def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    application.add_handler(conv_handler)
    
    # Запуск бота с polling
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    # Запускаем приложение без использования asyncio.run()
    asyncio.get_event_loop().run_until_complete(main())