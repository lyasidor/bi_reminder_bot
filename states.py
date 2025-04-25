from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
import datetime

# Состояния для ввода данных
TIME, TASK_NAME, REMINDER_TIME = range(3)

# Функция для старта процесса добавления задачи
async def add_task_start(update, context):
    await update.message.reply_text("Введите название задачи:")
    return TASK_NAME

# Функция для получения имени задачи
async def task_name(update, context):
    context.user_data['task_name'] = update.message.text
    await update.message.reply_text("Введите время выполнения задачи в формате ЧЧ:ММ:")
    return TIME

# Функция для получения времени выполнения задачи
async def task_time(update, context):
    try:
        time_str = update.message.text
        task_time = datetime.strptime(time_str, "%H:%M").time()
        context.user_data['task_time'] = task_time
        await update.message.reply_text("Введите время для напоминания (в минутах):")
        return REMINDER_TIME
    except ValueError:
        await update.message.reply_text("Неверный формат времени. Попробуйте снова.")
        return TIME

# Функция для получения времени напоминания
async def reminder_time(update, context):
    try:
        reminder_time = int(update.message.text)
        context.user_data['reminder_time'] = reminder_time
        await update.message.reply_text(f"Задача '{context.user_data['task_name']}' будет добавлена.")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Время напоминания должно быть числом. Попробуйте снова.")
        return REMINDER_TIME

# Завершаем процесс добавления задачи
async def cancel(update, context):
    await update.message.reply_text("Процесс добавления задачи отменен.")
    return ConversationHandler.END

# ConversationHandler для обработки состояний
task_handler = ConversationHandler(
    entry_points=[CommandHandler('add_task', add_task_start)],
    states={
        TASK_NAME: [MessageHandler(filters.TEXT, task_name)],
        TIME: [MessageHandler(filters.TEXT, task_time)],
        REMINDER_TIME: [MessageHandler(filters.TEXT, reminder_time)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
