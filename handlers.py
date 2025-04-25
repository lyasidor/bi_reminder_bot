from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CommandHandler, filters
from tasks import tasks, get_new_task_id, get_local_time, generate_date_keyboard, get_timezone_by_location
from scheduler import plan_reminder

TASK_NAME, DATE, TIME, REMINDER, COMMENT = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши название задачи.")
    return TASK_NAME

async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_name'] = update.message.text
    await update.message.reply_text("Выбери дату события:", reply_markup=generate_date_keyboard())
    return DATE

async def task_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_date'] = update.message.text
    await update.message.reply_text("Введи время события в формате ЧЧ:ММ (например, 14:30)")
    return TIME

async def task_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime
    import pytz

    time_input = update.message.text.strip()
    user_date = context.user_data['task_date']
    user = update.effective_user

    task_datetime = datetime.strptime(f"{user_date} {time_input}", "%d-%m-%Y %H:%M")

    # Получаем координаты юзера (или временно Москва)
    user_timezone = pytz.timezone("Europe/Moscow")
    now = datetime.now(user_timezone)

    if task_datetime < now:
        await update.message.reply_text("Время уже прошло. Введите корректное.")
        return TIME

    context.user_data['task_time'] = time_input
    context.user_data['task_datetime'] = user_timezone.localize(task_datetime)
    await update.message.reply_text("За сколько минут до события напомнить?")
    return REMINDER

async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutes = int(update.message.text)
        context.user_data['reminder_time'] = minutes
        await update.message.reply_text("Добавь комментарий или напиши 'Пропустить'")
        return COMMENT
    except ValueError:
        await update.message.reply_text("Напиши количество минут цифрой.")
        return REMINDER

async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_comment'] = update.message.text if update.message.text.lower() != "пропустить" else ""
    task_id = get_new_task_id()
    context.user_data['user_id'] = update.effective_user.id
    tasks[task_id] = context.user_data.copy()
    plan_reminder(task_id)
    await update.message.reply_text("Задача добавлена! Напоминание будет отправлено.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def list_tasks_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_tasks = [t for t in tasks.values() if t['user_id'] == user_id]

    if not user_tasks:
        await update.message.reply_text("У вас нет задач.")
        return

    response = "Ваши задачи:\n\n"
    for t in user_tasks:
        response += f"📌 {t['task_name']} — {t['task_datetime'].strftime('%d-%m-%Y %H:%M')}\n"

    await update.message.reply_text(response)

def get_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_name)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_date)],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_time)],
            REMINDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, reminder)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, comment)],
        },
        fallbacks=[],
    )
