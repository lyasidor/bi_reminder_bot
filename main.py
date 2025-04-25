from telegram import Update
from telegram.ext import CallbackContext

# Функция для команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я ваш напоминатель. Используйте /help для получения информации.")

# Функция для команды /help
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("""
    Вот список доступных команд:
    /start - Приветственное сообщение
    /help - Помощь
    /list_tasks - Показать все задачи
    /add_task - Добавить новую задачу
    """)

# Функция для команды /list_tasks (отображает список задач)
async def list_tasks(update: Update, context: CallbackContext):
    # Пример вывода задач
    tasks = ["Задача 1", "Задача 2", "Задача 3"]
    tasks_list = "\n".join(tasks) if tasks else "Нет задач."
    await update.message.reply_text(f"Ваши задачи:\n{tasks_list}")

# Функция для команды /add_task (добавление задачи)
async def add_task(update: Update, context: CallbackContext):
    # Попросим пользователя ввести название задачи
    await update.message.reply_text("Введите название задачи:")
    # Логика для обработки введенной задачи будет здесь.

# Дополнительная обработка сообщений
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    # Дополнительная логика для обработки текстовых сообщений.
    if "напоминай" in text:
        await update.message.reply_text("Ок, я буду напоминать.")
    else:
        await update.message.reply_text("Я не совсем понял, что вы хотите. Попробуйте /help.")