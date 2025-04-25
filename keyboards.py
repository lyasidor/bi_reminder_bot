from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import datetime

def start_markup():
    return ReplyKeyboardMarkup([["Добавить задачу", "Список задач"]], resize_keyboard=True)

def back_markup():
    return ReplyKeyboardMarkup([["Назад"]], resize_keyboard=True)

def skip_or_back_markup():
    return ReplyKeyboardMarkup([["Пропустить", "Назад"]], resize_keyboard=True)

def generate_date_keyboard():
    today = datetime.date.today()
    buttons = []
    for i in range(0, 14):
        day = today + datetime.timedelta(days=i)
        buttons.append([InlineKeyboardButton(day.strftime("%d-%m-%Y"), callback_data=day.strftime("%d-%m-%Y"))])
    return InlineKeyboardMarkup(buttons)