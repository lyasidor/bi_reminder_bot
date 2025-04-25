import time
import httpx
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Включение логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Словарь для хранения состояния пользователей
user_progress = {}

# Функция с повторными попытками
async def send_message_with_retry(bot, chat_id, text, retries=5, delay=2):
    for attempt in range(retries):
        try:
            await bot.send_message(chat_id=chat_id, text=text)
            break  # Успех, выходим из цикла
        except httpx.RequestError as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (2 ** attempt))  # Экспоненциальное увеличение задержки
                continue  # Пытаемся снова
            else:
                raise  # После последней попытки выбрасываем исключение

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    # Сбрасываем прогресс пользователя
    if user_id in user_progress:
        del user_progress[user_id]

    try:
        # Сообщение о сбросе прогресса и приветствие
        await send_message_with_retry(context.bot, user_id, "Привет! Я сбросил прогресс и готов работать с тобой снова.")
        await send_message_with_retry(context.bot, user_id, "Чтобы начать, выбери одну из опций ниже:")

        # Создаем клавиатуру с кнопками
        keyboard = [
            [KeyboardButton("Добавить задачу ✅"), KeyboardButton("Список задач 📋")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        # Отправляем сообщение с кнопками
        await update.message.reply_text("Что хочешь сделать?", reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Ошибка при выполнении команды /start: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    try:
        await send_message_with_retry(context.bot, user_id, "Вот список доступных команд:\n/start - Начать взаимодействие с ботом\n/help - Получить помощь")
    except Exception as e:
        logger.error(f"Ошибка при выполнении команды /help: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик кнопки "Добавить задачу"
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    # Проверка прогресса, если нет - создаем его
    if user_id not in user_progress:
        user_progress[user_id] = {}

    # Стартуем процесс добавления задачи
    try:
        user_progress[user_id]['step'] = 'enter_task_name'
        await send_message_with_retry(context.bot, user_id, "Введите название задачи:")
    except Exception as e:
        logger.error(f"Ошибка при добавлении задачи: {e}")
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик кнопки "Список задач"
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    # Проверка прогресса, если нет задач - уведомляем
    if user_id not in user_progress or 'tasks' not in user_progress[user_id] or len(user_progress[user_id]['tasks']) == 0:
        await send_message_with_retry(context.bot, user_id, "У вас нет задач. Добавьте их с помощью кнопки 'Добавить задачу'.")
    else:
        tasks = user_progress[user_id]['tasks']
        task_list = "\n".join([f"{task['name']} - {task['time']}" for task in tasks])
        await send_message_with_retry(context.bot, user_id, f"Ваши задачи:\n{task_list}")

# Обработчик сообщений (например, для ввода названия задачи)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    if user_id not in user_progress:
        user_progress[user_id] = {}

    step = user_progress[user_id].get('step')

    # Ввод названия задачи
    if step == 'enter_task_name':
        task_name = update.message.text
        user_progress[user_id]['task_name'] = task_name
        user_progress[user_id]['step'] = 'enter_task_date'
        await send_message_with_retry(context.bot, user_id, f"Задача '{task_name}' добавлена. Теперь выбери дату:")

        # Отправляем пользователю кнопки с датами
        # Например, две недели вперед
        keyboard = [
            [KeyboardButton("25.04.2025"), KeyboardButton("26.04.2025"), KeyboardButton("27.04.2025")],
            [KeyboardButton("28.04.2025"), KeyboardButton("29.04.2025"), KeyboardButton("30.04.2025")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Выберите дату:", reply_markup=reply_markup)

    # Ввод времени задачи
    elif step == 'enter_task_date':
        selected_date = update.message.text
        user_progress[user_id]['date'] = selected_date
        user_progress[user_id]['step'] = 'enter_task_time'
        await send_message_with_retry(context.bot, user_id, f"Вы выбрали дату {selected_date}. Теперь введите время в формате 'ЧЧ:ММ' (например, 18:30):")

    # Ввод времени задачи
    elif step == 'enter_task_time':
        task_time = update.message.text
        if not task_time:
            await send_message_with_retry(context.bot, user_id, "Пожалуйста, введите время в формате 'ЧЧ:ММ'.")
        else:
            user_progress[user_id]['time'] = task_time
            user_progress[user_id]['step'] = 'enter_task_comment'
            await send_message_with_retry(context.bot, user_id, f"Вы выбрали время {task_time}. Теперь введите комментарий (или пропустите):")

    # Ввод комментария
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

# Главная функция для запуска бота
def main():
    application = Application.builder().token("YOUR_TOKEN").build()

    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add_task", add_task))
    application.add_handler(CommandHandler("list_tasks", list_tasks))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
