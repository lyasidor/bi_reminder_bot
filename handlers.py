from telegram import Update
from telegram.ext import ContextTypes
from keyboards import start_keyboard, task_date_keyboard, task_time_keyboard, cancel_keyboard
from states import STATES
import datetime
import pytz

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я твой напоминалка-бот. 😊\nВыбери действие:",
        reply_markup=start_keyboard()
    )
    return STATES.MAIN

# Добавление задачи (этапы)
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите название задачи:")
    return STATES.TASK_NAME

# Список задач
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Заменить на реальную логику извлечения задач
    tasks = ["Задача 1", "Задача 2"]
    response = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
    await update.message.reply_text(response, reply_markup=start_keyboard())
    return STATES.MAIN

# Ввод названия задачи
async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_name'] = update.message.text
    await update.message.reply_text("Выберите дату для задачи:", reply_markup=task_date_keyboard())
    return STATES.TASK_DATE

# Ввод даты задачи
async def task_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_date'] = update.message.text
    await update.message.reply_text("Введите время для задачи (формат: ЧЧ:ММ):")
    return STATES.TASK_TIME

# Ввод времени задачи
async def task_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_time_str = update.message.text.strip()
    try:
        task_time = datetime.datetime.strptime(task_time_str, "%H:%M")
        context.user_data['task_time'] = task_time
        await update.message.reply_text("Добавьте комментарий (или напишите 'Пропустить'):")
        return STATES.TASK_COMMENT
    except ValueError:
        await update.message.reply_text("Неверный формат времени! Попробуйте снова.")
        return STATES.TASK_TIME

# Ввод комментария к задаче
async def task_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comment = update.message.text if update.message.text.lower() != 'пропустить' else ""
    context.user_data['task_comment'] = comment
    # Сохраняем задачу (будет реализовано в tasks.py)
    await update.message.reply_text(f"Задача '{context.user_data['task_name']}' создана!")
    return STATES.MAIN

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено!", reply_markup=start_keyboard())
    return STATES.MAIN