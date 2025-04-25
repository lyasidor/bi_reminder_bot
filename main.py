from telegram.ext import Application
from handlers import conv_handler

async def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    application.add_handler(conv_handler)
    
    # Запуск бота
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
