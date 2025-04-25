from telegram import Update
from telegram.ext import CallbackContext

def handle_button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  # Добавлено await
    data = query.data
    if data == 'start':
        query.edit_message_text("Введите название задачи:")
        return ADD_TASK
    elif data.startswith('date_'):
        query.edit_message_text(f"Вы выбрали дату: {data[5:]}")
        return ENTER_TIME

# Пример обработчика для текстового ввода
async def handle_text(update: Update, context: CallbackContext):
    user_input = update.message.text
    if user_input:
        await update.message.reply_text(f"Вы ввели: {user_input}")  # Добавлено await
    else:
        await update.message.reply_text("Пожалуйста, введите текст.")  # Добавлено await