from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import logging

# Установим уровень логирования для отслеживания ошибок
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Шаги для ConversationHandler
SELECT_ACTION, ENTER_TASK_NAME, SELECT_DATE, ENTER_TIME, ENTER_COMMENT, VIEW_TASKS, BACK = range(7)

# Хранение задач (в реальной разработке лучше использовать базу данных)
tasks = []

# Функция старта
async def start(update: Update, context):
    keyboard = [
        [KeyboardButton("📅 Добавить задачу"), KeyboardButton("📝 Список задач")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я помогу тебе с задачами. Выбери действие:", reply_markup=reply_markup)
    return SELECT_ACTION

# Обработка выбора действия
async def action_handler(update: Update, context):
    user_input = update.message.text
    if user_input == "📅 Добавить задачу":
        await update.message.reply_text("Введите название задачи:")
        return ENTER_TASK_NAME
    elif user_input == "📝 Список задач":
        if tasks:
            task_buttons = [
                [KeyboardButton(f"{task['time']} | {task['date']}")]
                for task in tasks
            ]
            task_buttons.append([KeyboardButton("🔙 Назад")])
            reply_markup = ReplyKeyboardMarkup(task_buttons, resize_keyboard=True)
            await update.message.reply_text("Список задач:", reply_markup=reply_markup)
            return VIEW_TASKS
        else:
            await update.message.reply_text("У тебя нет задач.")
            return SELECT_ACTION

# Ввод названия задачи
async def enter_task_name(update: Update, context):
    task_name = update.message.text
    context.user_data['task_name'] = task_name
    await update.message.reply_text("Выбери дату задачи из предложенных:")
    return SELECT_DATE

# Выбор даты
async def select_date(update: Update, context):
    keyboard = [
        [KeyboardButton("25.04.2025"), KeyboardButton("26.04.2025"), KeyboardButton("27.04.2025")],
        [KeyboardButton("28.04.2025"), KeyboardButton("29.04.2025"), KeyboardButton("30.04.2025")],
        [KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите дату:", reply_markup=reply_markup)
    return ENTER_TIME

# Ввод времени
async def enter_time(update: Update, context):
    user_input = update.message.text
    if ":" in user_input and len(user_input.split(":")) == 2:
        context.user_data['task_time'] = user_input
        await update.message.reply_text("Если хочешь, можешь добавить комментарий, или просто нажми 'Пропустить'.")
        return ENTER_COMMENT
    else:
        await update.message.reply_text("Пожалуйста, введите время в формате 'ЧЧ:ММ'.")

# Ввод комментария
async def enter_comment(update: Update, context):
    user_input = update.message.text
    if user_input.lower() == "пропустить":
        context.user_data['task_comment'] = None
    else:
        context.user_data['task_comment'] = user_input

    # Добавляем задачу в список
    task = {
        'name': context.user_data['task_name'],
        'date': context.user_data['task_date'],
        'time': context.user_data['task_time'],
        'comment': context.user_data.get('task_comment', 'Нет комментария'),
    }
    tasks.append(task)

    # Возвращаем на начальную страницу
    keyboard = [
        [KeyboardButton("📅 Добавить задачу"), KeyboardButton("📝 Список задач")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Задача добавлена! Выбери следующее действие:", reply_markup=reply_markup)
    return SELECT_ACTION

# Просмотр задач
async def view_tasks(update: Update, context):
    task_buttons = [
        [KeyboardButton(f"{task['time']} | {task['date']}")]
        for task in tasks
    ]
    task_buttons.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(task_buttons, resize_keyboard=True)
    await update.message.reply_text("Выберите задачу для просмотра:", reply_markup=reply_markup)
    return VIEW_TASKS

# Удаление задачи
async def delete_task(update: Update, context):
    user_input = update.message.text
    task_to_delete = None
    for task in tasks:
        if f"{task['time']} | {task['date']}" == user_input:
            task_to_delete = task
            break

    if task_to_delete:
        tasks.remove(task_to_delete)
        await update.message.reply_text("Задача удалена!")
    else:
        await update.message.reply_text("Задача не найдена.")
    
    return VIEW_TASKS

# Главное меню
async def back_to_main_menu(update: Update, context):
    keyboard = [
        [KeyboardButton("📅 Добавить задачу"), KeyboardButton("📝 Список задач")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return SELECT_ACTION

# Основная функция
def main():
    application = Application.builder().token("YOUR_BOT_API_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), MessageHandler(filters.TEXT, action_handler)],
        states={
            SELECT_ACTION: [MessageHandler(filters.TEXT, action_handler)],
            ENTER_TASK_NAME: [MessageHandler(filters.TEXT, enter_task_name)],
            SELECT_DATE: [MessageHandler(filters.TEXT, select_date)],
            ENTER_TIME: [MessageHandler(filters.TEXT, enter_time)],
            ENTER_COMMENT: [MessageHandler(filters.TEXT, enter_comment)],
            VIEW_TASKS: [MessageHandler(filters.TEXT, view_tasks)],
            BACK: [MessageHandler(filters.TEXT, back_to_main_menu)],
        },
        fallbacks=[MessageHandler(filters.TEXT, back_to_main_menu)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
