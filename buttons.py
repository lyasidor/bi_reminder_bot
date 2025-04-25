from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Основная клавиатура (Start)
def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("➕ Добавить задачу", callback_data="add_task")],
        [InlineKeyboardButton("📋 Список задач", callback_data="show_tasks")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для списка задач
def task_keyboard():
    keyboard = [
        [InlineKeyboardButton("⬅ Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для деталей задачи
def task_details_keyboard():
    keyboard = [
        [InlineKeyboardButton("❌ Удалить задачу", callback_data="delete_task")],
        [InlineKeyboardButton("⬅ Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)