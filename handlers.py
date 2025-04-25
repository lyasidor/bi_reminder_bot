from telegram import Update
from telegram.ext import ContextTypes
import datetime

# Состояния
TASK_NAME, TASK_DATE, TASK_TIME, TASK_COMMENT = range(4)

# Список задач (для примера)
tasks = []

# Функция для ввода названия задачи
async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_name'] = update.message.text
    await update.message.reply_text("Выберите дату события (например, 25.04.2025):")
    return TASK_DATE

# Функция для ввода даты
async def task_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_date'] = update.message.text
    await update.message.reply_text("Введите время события (формат ЧЧ:ММ):")
    return TASK_TIME

# Функция для ввода времени
async def time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем введённое время
        task_time = update.message.text.strip()

        # Проверка формата времени
        task_datetime_str = f"{context.user_data['task_date']} {task_time}"
        task_datetime = datetime.datetime.strptime(task_datetime_str, "%d-%m-%Y %H:%M")

        # Проверка на время в прошлом
        if task_datetime < datetime.datetime.now():
            await update.message.reply_text("Вы ввели время в прошлом. Пожалуйста, укажите корректное время.")
            return TASK_TIME  # Повторный запрос на время

        # Сохраняем время в user_data
        context.user_data['task_time'] = task_time
        await update.message.reply_text("Пожалуйста, напишите комментарий к задаче (или напишите 'Пропустить' для пропуска).")
        return TASK_COMMENT
    except ValueError:
        # Если формат времени неверен
        await update.message.reply_text("Неверный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ.")
        return TASK_TIME

# Функция для ввода комментария
async def task_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comment = update.message.text
    if comment.lower() != 'пропустить':
        context.user_data['task_comment'] = comment
    else:
        context.user_data['task_comment'] = "Без комментариев"

    # Создаём задачу
    task = {
        "task_name": context.user_data['task_name'],
        "task_date": context.user_data['task_date'],
        "task_time": context.user_data['task_time'],
        "task_comment": context.user_data['task_comment'],
    }

    # Сохраняем задачу (например, в списке задач)
    tasks.append(task)

    # Завершаем создание задачи
    await update.message.reply_text("Задача успешно создана! Теперь можно вернуться на главную страницу.")
    return ConversationHandler.END