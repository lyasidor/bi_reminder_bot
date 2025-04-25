from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from tasks import task_list

def start_buttons():
    keyboard = [
        [InlineKeyboardButton("Добавить задачу ✏️", callback_data='add_task')],
        [InlineKeyboardButton("Список задач 📋", callback_data='show_tasks')]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    keyboard = [
        [InlineKeyboardButton("Назад 🔙", callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)

def task_buttons():
    keyboard = []
    for i, task in enumerate(task_list):
        keyboard.append([InlineKeyboardButton(f"{task.time} {task.date}", callback_data=f"delete_task_{i}")])
    
    return keyboard
