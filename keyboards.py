from telegram import ReplyKeyboardMarkup

# Главное меню
def start_keyboard():
    return ReplyKeyboardMarkup([["Добавить задачу", "Список задач"]], resize_keyboard=True)

# Клавиатура для выбора даты
def task_date_keyboard():
    two_weeks_from_now = [datetime.date.today() + datetime.timedelta(days=i) for i in range(14)]
    buttons = [[f"{date.strftime('%d.%m.%Y')}" for date in two_weeks_from_now[i:i+3]] for i in range(0, len(two_weeks_from_now), 3)]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# Клавиатура для выбора времени
def task_time_keyboard():
    return ReplyKeyboardMarkup([["16:00", "18:00", "20:00"]], resize_keyboard=True)

# Клавиатура для пропуска
def cancel_keyboard():
    return ReplyKeyboardMarkup([["Пропустить"]], resize_keyboard=True)
