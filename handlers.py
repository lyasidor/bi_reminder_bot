from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database import add_task_to_db, get_tasks_from_db, delete_task_from_db, get_task_by_id
from datetime import datetime, timedelta

# Приветственное сообщение и кнопки
async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("➕ Добавить задачу", callback_data="add_task")],
        [InlineKeyboardButton("📝 Список задач", callback_data="show_tasks")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я твой бот-напоминалка. Что ты хочешь сделать?",
        reply_markup=reply_markup
    )
    return 0

# Начало добавления задачи
async def add_task(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Напиши название задачи."
    )
    return 1

# Обработка названия задачи
async def task_name(update: Update, context: CallbackContext) -> int:
    context.user_data['task_name'] = update.message.text
    # Генерация кнопок для выбора даты
    today = datetime.today()
    dates = [today + timedelta(days=i) for i in range(14)]
    keyboard = [[InlineKeyboardButton(date.strftime('%d.%m.%Y'), callback_data=f"date_{date.strftime('%d.%m.%Y')}") for date in dates[i:i+3]] for i in range(0, len(dates), 3)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите дату задачи:", reply_markup=reply_markup)
    return 2

# Обработка даты задачи
async def task_date(update: Update, context: CallbackContext) -> int:
    context.user_data['task_date'] = update.message.text
    await update.message.reply_text(
        "Теперь укажи время задачи (формат: ЧЧ:ММ)."
    )
    return 3

# Обработка времени задачи
async def task_time(update: Update, context: CallbackContext) -> int:
    try:
        time_input = update.message.text
        hour, minute = map(int, time_input.split(":"))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError
        context.user_data['task_time'] = time_input
        await update.message.reply_text(
            "Задача создана! Теперь, если хочешь, можешь ввести комментарий или просто пропустить."
        )
        return 4
    except ValueError:
        await update.message.reply_text("Неверный формат времени! Попробуй снова (ЧЧ:ММ).")
        return 3

# Обработка комментария
async def task_comment(update: Update, context: CallbackContext) -> int:
    context.user_data['task_comment'] = update.message.text if update.message.text.lower() != 'пропустить' else None
    # Сохранение задачи в базе данных
    add_task_to_db(context.user_data['task_name'], context.user_data['task_date'], context.user_data['task_time'], context.user_data.get('task_comment'))
    await update.message.reply_text("Задача добавлена!")
    return 0

# Показать задачи
async def show_tasks(update: Update, context: CallbackContext) -> int:
    tasks = get_tasks_from_db()
    keyboard = [
        [InlineKeyboardButton(f"{task['name']} - {task['date']} - {task['time']}", callback_data=f"task_details_{task['id']}") for task in tasks]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Список задач:", reply_markup=reply_markup)
    return 0

# Показать детали задачи
async def task_details(update: Update, context: CallbackContext) -> int:
    task_id = update.callback_query.data.split("_")[2]
    task = get_task_by_id(task_id)
    details = f"Задача: {task['name']}\nДата: {task['date']}\nВремя: {task['time']}\nКомментарий: {task['comment'] if task['comment'] else 'Нет'}"
    keyboard = [
        [InlineKeyboardButton("❌ Удалить задачу", callback_data=f"delete_task_{task['id']}")],
        [InlineKeyboardButton("🔙 Назад", callback_data="show_tasks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(details, reply_markup=reply_markup)
    return 0

# Удалить задачу
async def delete_task(update: Update, context: CallbackContext) -> int:
    task_id = update.callback_query.data.split("_")[2]
    delete_task_from_db(task_id)
    await update.callback_query.message.edit_text("Задача удалена!")
    return 0