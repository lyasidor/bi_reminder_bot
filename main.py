import os
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

load_dotenv() 

TOKEN = "7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o"  # Получаем токен из переменной окружения

# Функция для команды /start
async def start(update: Update, context):
    # Приветственное сообщение
    await update.message.reply_text("Привет! Я бот-напоминалка 😊. Выбери одно из действий ниже:", reply_markup=start_buttons())

# Функция для кнопок на старте
def start_buttons():
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton("Добавить задачу 📅", callback_data='add_task')],
        [InlineKeyboardButton("Список задач 📋", callback_data='list_tasks')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Основная функция для запуска бота
def main():
    # Создаём приложение с токеном, без параметра use_context
    application = Application.builder().token(TOKEN).build()

    # Обработчики
    application.add_handler(CommandHandler("start", start))
    
    # Дополнительные обработчики для кнопок, сообщений, и других команд
    # Например, для обработки нажатия на кнопки:
    application.add_handler(CallbackQueryHandler(callback_query_handler))

    # Запуск бота
    application.run_polling()

# Обработчик нажатия на кнопки
async def callback_query_handler(update: Update, context):
    query = update.callback_query
    if query.data == 'add_task':
        await query.answer("Добавление задачи...")
    elif query.data == 'list_tasks':
        await query.answer("Список задач...")

if __name__ == "__main__":
    main()

