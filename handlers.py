import tasks
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
)
from keyboards import start_markup, generate_date_keyboard, back_markup, skip_or_back_markup
from states import States
from tasks import create_task, get_user_tasks, delete_task, get_task_by_id

# Хранилище временных данных пользователей
user_data_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Что будем делать?", reply_markup=start_markup())
    return ConversationHandler.END

async def start_add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_store[update.effective_user.id] = {"history": []}
    await update.message.reply_text("Какую задачу добавишь?", reply_markup=back_markup())
    return States.TASK_NAME

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tasks:
        await update.message.reply_text("У тебя нет задач.", reply_markup=start_markup)
        return
    message = "\n".join([f"{i}. {t['task_name']} — {t['task_date']} {t['task_time']}" for i, t in tasks.items()])
    await update.message.reply_text("Список задач:\n\n" + message, reply_markup=start_markup)

async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🔙 Назад":
        return await start(update, context)
    context.user_data["task_name"] = text
    await update.message.reply_text("Выбери дату", reply_markup=generate_date_keyboard())
    return States.DATE

async def task_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🔙 Назад":
        await update.message.reply_text("Какую задачу добавишь?", reply_markup=back_markup())
        return States.TASK_NAME
    context.user_data["task_date"] = text
    await update.message.reply_text("Напиши время в формате ЧЧ:ММ (например, 18:24)", reply_markup=back_markup())
    return States.TIME

async def task_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🔙 Назад":
        await update.message.reply_text("Выбери дату", reply_markup=generate_date_keyboard())
        return States.DATE
    if not text or not validate_time_format(text):
        await update.message.reply_text("Введи корректное время в формате ЧЧ:ММ")
        return States.TIME
    context.user_data["task_time"] = text
    await update.message.reply_text("Напиши в минутах, за сколько времени до начала события я должен тебя предупредить", reply_markup=back_markup())
    return States.REMINDER_MINUTES

async def task_minutes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🔙 Назад":
        await update.message.reply_text("Напиши время в формате ЧЧ:ММ (например, 18:24)", reply_markup=back_markup())
        return States.TIME
    if not text.isdigit():
        await update.message.reply_text("Введи число минут")
        return States.REMINDER_MINUTES
    context.user_data["reminder_minutes"] = int(text)
    await update.message.reply_text("Введи комментарий к задаче или нажми 'Пропустить'", reply_markup=skip_or_back_markup())
    return States.COMMENT

async def task_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🔙 Назад":
        await update.message.reply_text("Напиши в минутах, за сколько времени до начала события я должен тебя предупредить", reply_markup=back_markup())
        return States.REMINDER_MINUTES
    context.user_data["comment"] = None if text == "Пропустить" else text

    # Сохранение задачи
    user_id = update.effective_user.id
    create_task(user_id, context.user_data)

    await update.message.reply_text("Задача успешно создана!", reply_markup=start_markup())
    return ConversationHandler.END

async def task_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = get_user_tasks(user_id)

    if not tasks:
        await update.message.reply_text("У тебя пока нет задач.", reply_markup=start_markup())
        return ConversationHandler.END

    reply = "Вот твои задачи:\n\n"
    keyboard = []
    row = []

    for i, task in enumerate(tasks[:10], 1):
        btn = f"{i}. {task['name']}"
        row.append(btn)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append(["🔙 Назад"])

    context.user_data["tasks"] = tasks
    await update.message.reply_text(reply, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return States.TASK_VIEW

async def task_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🔙 Назад":
        return await start(update, context)
    
    if not text[0].isdigit():
        await update.message.reply_text("Выбери задачу из списка.")
        return States.TASK_VIEW

    index = int(text.split(".")[0]) - 1
    task = context.user_data["tasks"][index]
    context.user_data["current_task"] = task

    reply = (
        f"Название задачи: {task['name']}\n"
        f"{task['date']}, {task['time']}\n\n"
        f"{task.get('comment', 'Без комментария')}"
    )
    keyboard = [["Удалить задачу"], ["🔙 Назад"]]
    await update.message.reply_text(reply, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return States.TASK_ACTION

async def task_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🔙 Назад":
        return await task_list(update, context)

    if text == "Удалить задачу":
        delete_task(update.effective_user.id, context.user_data["current_task"])
        await update.message.reply_text("Задача удалена.", reply_markup=start_markup())
        return ConversationHandler.END

def validate_time_format(time_str):
    try:
        hours, minutes = map(int, time_str.split(":"))
        return 0 <= hours < 24 and 0 <= minutes < 60
    except:
        return False

def get_conv_handler():
    return ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^➕ Добавить задачу$"), start_add_task),
            MessageHandler(filters.Regex("^📋 Список задач$"), task_list)
        ],
        states={
            States.TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_name)],
            States.DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_date)],
            States.TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_time)],
            States.REMINDER_MINUTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_minutes)],
            States.COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_comment)],
            States.TASK_VIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_view)],
            States.TASK_ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_action)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
