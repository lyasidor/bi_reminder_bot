from telegram import ReplyKeyboardMarkup, Update, KeyboardButton
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, MessageHandler, filters
from task_manager import TaskManager
from datetime import datetime, timedelta
import pytz

# Состояния для ConversationHandler
ADD_TASK, ENTER_DATE, ENTER_TIME, ENTER_COMMENT = range(4)

task_manager = TaskManager()

def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        f"Привет, {user.first_name}! Я бот-напоминалка. Выберите, что хотите сделать.",
        reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Добавить задачу ✍️"), KeyboardButton("Список задач 📋")],
        ], one_time_keyboard=True)
    )
    return ADD_TASK

def handle_button_click(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    if query.data == "Добавить задачу ✍️":
        return add_task(update, context)
    elif query.data == "Список задач 📋":
        return show_task_list(update, context)

def add_task(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Введите название задачи:")
    return ENTER_DATE

def handle_text(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text
    if context.user_data.get('task_name') is None:
        context.user_data['task_name'] = user_input
        update.message.reply_text("Выберите дату задачи на ближайшие 2 недели:", reply_markup=get_date_buttons())
        return ENTER_TIME
    elif context.user_data.get('task_date') is None:
        context.user_data['task_date'] = user_input
        update.message.reply_text("Введите время в формате 'ЧЧ:ММ':")
        return ENTER_COMMENT
    elif context.user_data.get('task_time') is None:
        context.user_data['task_time'] = user_input
        update.message.reply_text("Введите комментарий к задаче (или нажмите 'Пропустить'):")
        return ENTER_COMMENT
    else:
        context.user_data['task_comment'] = user_input
        task_manager.add_task(context.user_data)
        update.message.reply_text("Задача добавлена! Вернуться в меню.",
                                  reply_markup=ReplyKeyboardMarkup([
                                      [KeyboardButton("Добавить задачу ✍️"), KeyboardButton("Список задач 📋")]
                                  ], one_time_keyboard=True))
        return ConversationHandler.END

def get_date_buttons():
    # Создаём кнопки с датами на ближайшие две недели
    today = datetime.today()
    buttons = []
    for i in range(14):  # Делаем кнопки на 2 недели
        date_str = (today + timedelta(days=i)).strftime("%d.%m.%Y")
        buttons.append([KeyboardButton(date_str)])
    
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

def show_task_list(update: Update, context: CallbackContext) -> int:
    task_list = task_manager.get_task_list()
    if not task_list:
        update.message.reply_text("У вас нет задач.")
        return ConversationHandler.END

    # Формируем список задач в виде кнопок
    task_buttons = []
    for idx, task in enumerate(task_list):
        task_buttons.append([KeyboardButton(f"{task['time']}, {task['date']}")])
    
    update.message.reply_text("Ваши задачи:", reply_markup=ReplyKeyboardMarkup(task_buttons))
    return ADD_TASK

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ADD_TASK: [MessageHandler(filters.TEXT, handle_button_click)],
        ENTER_DATE: [MessageHandler(filters.TEXT, handle_text)],
        ENTER_TIME: [MessageHandler(filters.TEXT, handle_text)],
        ENTER_COMMENT: [MessageHandler(filters.TEXT, handle_text)],
    },
    fallbacks=[CommandHandler('start', start)],
)