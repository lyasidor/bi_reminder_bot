from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from buttons import start_buttons, back_button, task_buttons
from tasks import Task, task_list

# Стартовое приветствие
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Я ваш бот-напоминалка. Выберите, что хотите сделать:",
        reply_markup=start_buttons()
    )

# Добавление задачи
def add_task(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data['step'] = 'task_name'

    query.edit_message_text(
        text="Введите название задачи:",
        reply_markup=back_button()
    )

# Показ задач
def show_tasks(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    task_list_buttons = task_buttons()
    query.edit_message_text(
        text="Список ваших задач:",
        reply_markup=InlineKeyboardMarkup(task_list_buttons)
    )

# Удаление задачи
def delete_task(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    task_index = int(query.data.split("_")[2])
    task = task_list.pop(task_index)

    query.edit_message_text(
        text=f"Задача '{task.name}' была удалена.",
        reply_markup=start_buttons()
    )
