from telegram import Update
from telegram.ext import CallbackContext

ADD_TASK, ENTER_TIME, ENTER_COMMENT = range(3)  # Пример состояний для ConversationHandler

def handle_button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    if data == 'start':
        query.edit_message_text("Введите название задачи:")
        return ADD_TASK
    elif data.startswith('date_'):
        query.edit_message_text(f"Вы выбрали дату: {data[5:]}")
        return ENTER_TIME

async def handle_text(update: Update, context: CallbackContext):
    user_input = update.message.text
    if user_input:
        await update.message.reply_text(f"Вы ввели: {user_input}")
    else:
        await update.message.reply_text("Пожалуйста, введите текст.")

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    keyboard = [['Добавить задачу'], ['Список задач']]
    reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True, 'resize_keyboard': True}
    await update.message.reply_text("Привет! Чем могу помочь?", reply_markup=reply_markup)
    return ADD_TASK  # Переход к состоянию добавления задачи