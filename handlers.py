from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler
from telegram.ext import CallbackContext

# Определение состояний для ConversationHandler
TASK_NAME, TASK_DATE, TASK_TIME, TASK_COMMENT = range(4)

# Функция для обработки команды /start
async def task_name(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Привет! Давай начнем. Напиши название задачи."
    )
    return TASK_NAME

# Функция для обработки ввода названия задачи
async def task_name(update: Update, context: CallbackContext) -> int:
    context.user_data['task_name'] = update.message.text
    await update.message.reply_text(
        "Отлично! Теперь выбери дату задачи."
    )
    return TASK_DATE

# Функция для обработки ввода даты
async def task_date(update: Update, context: CallbackContext) -> int:
    context.user_data['task_date'] = update.message.text
    await update.message.reply_text(
        "Теперь, напиши время задачи в формате ЧЧ:ММ."
    )
    return TASK_TIME

# Функция для обработки ввода времени
async def time(update: Update, context: CallbackContext) -> int:
    try:
        time_input = update.message.text
        # Валидация формата времени
        hour, minute = map(int, time_input.split(":"))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError("Неверный формат времени.")
        context.user_data['task_time'] = time_input
        await update.message.reply_text(
            "Здорово! Теперь, если хочешь, можешь ввести комментарий к задаче, или просто напиши 'Пропустить'."
        )
        return TASK_COMMENT
    except ValueError:
        await update.message.reply_text(
            "Ошибка! Пожалуйста, введите время в формате ЧЧ:ММ."
        )
        return TASK_TIME

# Функция для обработки комментария
async def task_comment(update: Update, context: CallbackContext) -> int:
    context.user_data['task_comment'] = update.message.text if update.message.text.lower() != 'пропустить' else None
    # Возвращаем пользователя на начальный экран или показываем какие-то данные
    await update.message.reply_text("Задача успешно добавлена! Смотри свой список задач.")
    return ConversationHandler.END
