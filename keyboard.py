from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_task_buttons(text: str, callback_data: str) -> InlineKeyboardButton:
    """
    Функция для создания кнопки с текстом и callback_data.
    :param text: текст кнопки
    :param callback_data: данные для обработки нажатия на кнопку
    :return: объект InlineKeyboardButton
    """
    return InlineKeyboardButton(text, callback_data=callback_data)

def get_main_menu_buttons():
    """
    Функция для создания кнопок главного меню.
    :return: объект InlineKeyboardMarkup с кнопками
    """
    buttons = [
        [get_task_buttons('Добавить задачу ✍️', 'add_task')],
        [get_task_buttons('Список задач 📋', 'view_tasks')]
    ]
    return InlineKeyboardMarkup(buttons)

# Кнопка "Назад"
def get_back_button():
    """
    Функция для создания кнопки "Назад".
    :return: объект InlineKeyboardButton
    """
    return InlineKeyboardButton('Назад', callback_data='back')
