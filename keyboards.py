from telegram import ReplyKeyboardMarkup

# Клавиатуры для бота
main_menu_keyboard = [
    ['Добавить задачу', 'Список задач'],
]

add_task_keyboard = [
    ['Назад'],
]

back_to_main_keyboard = [
    ['Назад'],
]

# Формирование клавиатуры
def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

def get_add_task_keyboard():
    return ReplyKeyboardMarkup(add_task_keyboard, resize_keyboard=True)

def get_back_to_main_keyboard():
    return ReplyKeyboardMarkup(back_to_main_keyboard, resize_keyboard=True)
