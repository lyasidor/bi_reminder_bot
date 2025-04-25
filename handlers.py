from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from database import add_task_to_db, get_tasks_from_db, delete_task_from_db
from keyboard import get_back_button, get_task_list_buttons, get_task_buttons

TASK_NAME, TASK_DATE, TASK_TIME, TASK_COMMENT = range(4)

# Приветствие и начало
async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [get_task_buttons('Добавить задачу'), get_task_buttons('Список задач')]
    ]
    await update.message.reply_text("Привет! Я помогу тебе с задачами. Что ты хочешь сделать?", reply_markup=keyboard)
    return TASK_NAME

# Обработка ввода названия задачи
async def task_name(update: Update, context: CallbackContext) -> int:
    context.user_data['task_name'] = update.message.text
    keyboard = [get_back_button()]
    await update.message.reply_text("Отлично! Теперь выбери дату задачи.", reply_markup=keyboard)
    return TASK_DATE

# Обработка ввода даты задачи
async def task_date(update: Update, context: CallbackContext) -> int:
    context.user_data['task_date'] = update.message.text
    keyboard = [get_back_button()]
    await update.message.reply_text("Теперь укажи время задачи в формате ЧЧ:ММ.", reply_markup=keyboard)
    return TASK_TIME

# Обработка времени
async def time(update: Update, context: CallbackContext) -> int:
    try:
        time_input = update.message.text
        hour, minute = map(int, time_input.split(":"))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError("Неверный формат времени.")
        context.user_data['task_time'] = time_input
        keyboard = [get_back_button()]
        await update.message.reply_text("Здорово! Если хочешь, можешь ввести комментарий или пропустить.", reply_markup=keyboard)
        return TASK_COMMENT
    except ValueError:
        await update.message.reply_text("Ошибка! Введите время в формате ЧЧ:ММ.")
        return TASK_TIME

# Обработка комментария
async def task_comment(update: Update, context: CallbackContext) -> int:
    context.user_data['task_comment'] = update.message.text if update.message.text.lower() != 'пропустить' else None
    add_task_to_db(context.user_data['task_name'], context.user_data['task_date'], context.user_data['task_time'], context.user_data['task_comment'])
    keyboard = [get_back_button()]
    await update.message.reply_text("Задача добавлена! Вернуться в главное меню.", reply_markup=keyboard)
    return ConversationHandler.END

# Отображение задач
async def show_tasks(update: Update, context: CallbackContext) -> None:
    tasks = get_tasks_from_db()
    task_buttons = get_task_list_buttons(tasks)
    keyboard = task_buttons + [get_back_button()]
    await update.callback_query.message.edit_text("Ваши задачи:", reply_markup=keyboard)

# Удаление задачи
async def delete_task(update: Update, context: CallbackContext) -> None:
    task_id = update.callback_query.data.split('_')[2]
    delete_task_from_db(task_id)
    tasks = get_tasks_from_db()
    task_buttons = get_task_list_buttons(tasks)
    keyboard = task_buttons + [get_back_button()]
    await update.callback_query.message.edit_text("Задача удалена. Ваши задачи:", reply_markup=keyboard)