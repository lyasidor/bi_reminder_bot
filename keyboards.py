from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# Клавиатура для основного меню
def start_keyboard():
    keyboard = [
        [KeyboardButton('Показать задачи')],
        [KeyboardButton('Добавить задачу')]
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

# Клавиатура для выбора действия с задачей
def task_action_keyboard():
    keyboard = [
        [InlineKeyboardButton('Изменить задачу', callback_data='edit_task')],
        [InlineKeyboardButton('Удалить задачу', callback_data='delete_task')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для подтверждения действия (например, подтверждения удаления)
def confirmation_keyboard():
    keyboard = [
        [InlineKeyboardButton('Да', callback_data='yes')],
        [InlineKeyboardButton('Нет', callback_data='no')]
    ]
    return InlineKeyboardMarkup(keyboard)
