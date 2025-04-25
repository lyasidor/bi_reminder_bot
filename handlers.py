from telegram import Update
from telegram.ext import CallbackContext
from tasks import add_new_task, get_task_list, get_task_details, delete_task
from buttons import task_keyboard, task_details_keyboard, main_keyboard

# Стартовое приветственное сообщение и клавиатура
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Я помогу тебе с напоминаниями. Что ты хочешь сделать?",
        reply_markup=main_keyboard()
    )

# Добавить задачу
def add_task(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Пожалуйста, введите название задачи:", reply_markup=None)
    return "WAITING_FOR_TASK_NAME"

# Показать список задач
def show_tasks(update: Update, context: CallbackContext):
    task_list = get_task_list()  # Получаем задачи из базы данных/файла
    if not task_list:
        update.callback_query.edit_message_text("У вас нет задач. Добавьте новую задачу.", reply_markup=main_keyboard())
    else:
        # Отправляем список задач с кнопками для удаления
        reply_text = "Ваши задачи:\n\n"
        for task in task_list:
            reply_text += f"{task['time']} - {task['date']} - {task['name']}\n"
        update.callback_query.edit_message_text(reply_text, reply_markup=task_keyboard())
    return "SHOWING_TASKS"

# Обработка выбора задачи для просмотра подробностей
def handle_task_selection(update: Update, context: CallbackContext):
    task_id = update.callback_query.data.split("_")[1]
    task = get_task_details(task_id)  # Получаем подробности задачи по ID
    task_details = f"Задача: {task['name']}\nДата: {task['date']}\nВремя: {task['time']}\nКомментарий: {task.get('comment', 'Нет комментария')}"
    update.callback_query.edit_message_text(task_details, reply_markup=task_details_keyboard())
    return "SHOW_TASK_DETAILS"