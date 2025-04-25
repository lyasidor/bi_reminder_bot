from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext
from utils import send_message_with_retry
import logging

# Логирование ошибок
logger = logging.getLogger(__name__)

# Словарь для хранения данных о пользователях
user_progress = {}

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    # Сбрасываем прогресс пользователя
    if user_id in user_progress:
        del user_progress[user_id]

    try:
        await send_message_with_retry(context.bot, user_id, "Привет! Я сбросил прогресс. Чтобы начать, выбери одну из опций ниже:")

        # Клавиатура
        keyboard = [
            [KeyboardButton("Добавить задачу ✅"), KeyboardButton("Список задач 📋")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Что хочешь сделать?", reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Ошибка при обработке /start: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик команды /help
async def help_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    try:
        await send_message_with_retry(context.bot, user_id, "Вот список доступных команд:\n/start - Начать взаимодействие с ботом\n/help - Получить помощь")
    except Exception as e:
        logger.error(f"Ошибка при обработке /help: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик кнопки "Добавить задачу"
async def add_task(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    # Проверяем прогресс
    if user_id not in user_progress:
        user_progress[user_id] = {}

    try:
        user_progress[user_id]['step'] = 'enter_task_name'
        await send_message_with_retry(context.bot, user_id, "Введите название задачи:")
    except Exception as e:
        logger.error(f"Ошибка при добавлении задачи: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик кнопки "Список задач"
async def list_tasks(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    # Проверка на наличие задач
    if user_id not in user_progress or 'tasks' not in user_progress[user_id] or len(user_progress[user_id]['tasks']) == 0:
        await send_message_with_retry(context.bot, user_id, "У вас нет задач. Добавьте их с помощью кнопки 'Добавить задачу'.")
    else:
        tasks = user_progress[user_id]['tasks']
        task_list = "\n".join([f"{task['name']} - {task['time']}" for task in tasks])
        await send_message_with_retry(context.bot, user_id, f"Ваши задачи:\n{task_list}")

# Обработчик сообщений от пользователя (например, ввод названия задачи)
async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    if user_id not in user_progress:
        user_progress[user_id] = {}

    step = user_progress[user_id].get('step')

    if step == 'enter_task_name':
        task_name = update.message.text
        user_progress[user_id]['task_name'] = task_name
        user_progress[user_id]['step'] = 'enter_task_date'
        await send_message_with_retry(context.bot, user_id, f"Задача '{task_name}' добавлена. Теперь выбери дату:")

        # Отправляем кнопки с датами
        keyboard = [
            [KeyboardButton("25.04.2025"), KeyboardButton("26.04.2025"), KeyboardButton("27.04.2025")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Выберите дату:", reply_markup=reply_markup)

    elif step == 'enter_task_date':
        selected_date = update.message.text
        user_progress[user_id]['date'] = selected_date
        user_progress[user_id]['step'] = 'enter_task_time'
        await send_message_with_retry(context.bot, user_id, f"Вы выбрали дату {selected_date}. Теперь введите время в формате 'ЧЧ:ММ'.")

    elif step == 'enter_task_time':
        task_time = update.message.text
        user_progress[user_id]['time'] = task_time
        user_progress[user_id]['step'] = 'enter_task_comment'
        await send_message_with_retry(context.bot, user_id, f"Вы выбрали время {task_time}. Теперь введите комментарий (или пропустите):")

    elif step == 'enter_task_comment':
        task_comment = update.message.text
        user_progress[user_id]['comment'] = task_comment
        user_progress[user_id]['step'] = 'task_added'

        # Добавляем задачу в список задач
        if 'tasks' not in user_progress[user_id]:
            user_progress[user_id]['tasks'] = []

        user_progress[user_id]['tasks'].append({
            'name': user_progress[user_id]['task_name'],
            'date': user_progress[user_id]['date'],
            'time': user_progress[user_id]['time'],
            'comment': user_progress[user_id].get('comment', '')
        })

        await send_message_with_retry(context.bot, user_id, "Задача добавлена!")
        user_progress[user_id] = {}  # Сбрасываем прогресс
        await start(update, context)

# Обработчик для кнопок
async def handle_button_click(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    button_text = update.message.text

    if button_text == "Добавить задачу ✅":
        await add_task(update, context)
    elif button_text == "Список задач 📋":
        await list_tasks(update, context)

# Добавляем обработчики команд
start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help_command)
add_task_handler = MessageHandler(filters.TEXT & filters.Regex("Добавить задачу ✅"), handle_button_click)
list_tasks_handler = MessageHandler(filters.TEXT & filters.Regex("Список задач 📋"), handle_button_click)
message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
