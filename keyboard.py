from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Создаем клавиатуру для главного меню
def start_keyboard():
    keyboard = [
        [InlineKeyboardButton("Добавить задачу ✍️", callback_data='add_task')],
        [InlineKeyboardButton("Список задач 📋", callback_data='list_tasks')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для кнопок "Назад"
def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Назад 🔙", callback_data='back')]])

# Клавиатура с выбором даты
def date_keyboard(dates):
    keyboard = [[InlineKeyboardButton(date, callback_data=f'date_{date}')] for date in dates]
    return InlineKeyboardMarkup(keyboard)

# Клавиатура для ввода времени
def time_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Пропустить ⏩", callback_data='skip_time')]])
