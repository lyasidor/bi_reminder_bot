from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

tasks = []  # Список для хранения задач
MAX_TASKS = 10  # Максимальное количество задач

def start(update: Update, context: CallbackContext) -> None:
    """Приветственное сообщение и кнопки"""
    keyboard = [
        [InlineKeyboardButton("Добавить задачу 📝", callback_data='add_task')],
        [InlineKeyboardButton("Список задач 📋", callback_data='show_tasks')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! Чем могу помочь?", reply_markup=reply_markup)

def add_task(update: Update, context: CallbackContext) -> None:
    """Запрос на ввод названия задачи"""
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Пожалуйста, введите название задачи:", reply_markup=reply_markup)

def save_task(update: Update, context: CallbackContext) -> None:
    """Сохранение введенной задачи и переход к выбору даты"""
    context.user_data['task_name'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("25.04.2025", callback_data='2025-04-25')],
        [InlineKeyboardButton("26.04.2025", callback_data='2025-04-26')],
        [InlineKeyboardButton("27.04.2025", callback_data='2025-04-27')],
        [InlineKeyboardButton("Назад", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите дату для задачи:", reply_markup=reply_markup)

def set_time(update: Update, context: CallbackContext) -> None:
    """Запрос на ввод времени"""
    context.user_data['task_date'] = update.callback_query.data
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Пожалуйста, введите время задачи в формате ЧЧ:ММ.", reply_markup=reply_markup)

def save_time(update: Update, context: CallbackContext) -> None:
    """Сохранение времени и переход к вводу комментария"""
    context.user_data['task_time'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Пропустить", callback_data='skip')],
        [InlineKeyboardButton("Назад", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Если хотите, можете ввести комментарий к задаче:", reply_markup=reply_markup)

def save_comment(update: Update, context: CallbackContext) -> None:
    """Сохранение комментария или пропуск"""
    if update.message.text != "Пропустить":
        context.user_data['task_comment'] = update.message.text
    task = {
        'name': context.user_data['task_name'],
        'date': context.user_data['task_date'],
        'time': context.user_data['task_time'],
        'comment': context.user_data.get('task_comment', 'Нет комментариев')
    }
    if len(tasks) < MAX_TASKS:
        tasks.append(task)
    context.user_data.clear()  # Очистка данных пользователя
    keyboard = [
        [InlineKeyboardButton("Добавить задачу 📝", callback_data='add_task')],
        [InlineKeyboardButton("Список задач 📋", callback_data='show_tasks')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Задача добавлена! Вы можете вернуться на главный экран.", reply_markup=reply_markup)

def show_tasks(update: Update, context: CallbackContext) -> None:
    """Показать список задач"""
    if not tasks:
        update.message.reply_text("У вас нет задач.")
        return
    keyboard = []
    for task in tasks:
        task_str = f"{task['time']}, {task['date']}"
        keyboard.append([InlineKeyboardButton(task_str, callback_data=f"task_{task_str}")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Вот список ваших задач:", reply_markup=reply_markup)

def task_details(update: Update, context: CallbackContext) -> None:
    """Отображение подробной информации о задаче"""
    task_str = update.callback_query.data.split('_')[1]
    task = next((t for t in tasks if f"{t['time']}, {t['date']}" == task_str), None)
    if task:
        task_info = (
            f"Название задачи: {task['name']} 📝\n"
            f"Дата: {task['date']} 📅\n"
            f"Время: {task['time']} 🕒\n"
            f"Комментарий: {task['comment']}"
        )
        keyboard = [
            [InlineKeyboardButton("Удалить задачу 🗑️", callback_data=f"delete_{task_str}")],
            [InlineKeyboardButton("Назад", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text(task_info, reply_markup=reply_markup)

def delete_task(update: Update, context: CallbackContext) -> None:
    """Удаление задачи"""
    task_str = update.callback_query.data.split('_')[1]
    task = next((t for t in tasks if f"{t['time']}, {t['date']}" == task_str), None)
    if task:
        tasks.remove(task)
    show_tasks(update, context)  # Показать обновленный список задач

def button_handler(update: Update, context: CallbackContext) -> None:
    """Обработка нажатий кнопок"""
    query = update.callback_query
    query.answer()  # Подтверждение нажатия

    if query.data == 'add_task':
        add_task(update, context)
    elif query.data == 'show_tasks':
        show_tasks(update, context)
    elif query.data == 'back':
        start(update, context)  # Возвращаем на главный экран
    elif query.data.startswith('task_'):
        task_details(update, context)
    elif query.data.startswith('delete_'):
        delete_task(update, context)