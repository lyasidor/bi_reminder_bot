from telegram import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

def start_markup():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("➕ Добавить задачу")],
            [KeyboardButton("📋 Список задач")]
        ],
        resize_keyboard=True
    )

def generate_date_keyboard():
    today = datetime.now().date()
    keyboard = []
    row = []
    for i in range(14):
        day = today + timedelta(days=i)
        button = KeyboardButton(day.strftime("%d-%m-%Y"))
        row.append(button)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([KeyboardButton("🔙 Назад")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def skip_or_back_markup():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Пропустить")], [KeyboardButton("🔙 Назад")]],
        resize_keyboard=True
    )

def back_markup():
    return ReplyKeyboardMarkup([[KeyboardButton("🔙 Назад")]], resize_keyboard=True)