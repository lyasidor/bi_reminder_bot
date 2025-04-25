from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Твой токен
TOKEN = "7447545827:AAFf6HxnyeZRhbEGAPpMsS5jDwjzh-AO81o"

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
    
    # Дополнительные обработчики для кнопок
