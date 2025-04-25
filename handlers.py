from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from telegram.ext import CallbackContext

# Степы для ConversationHandler
ADD_TASK, ENTER_TIME, ENTER_COMMENT = range(3)

# start — обработка команды /start
async def start(update: Update, context: CallbackContext) -> int:
    # Код обработки /start
    await update.message.reply_text("Привет! Давай начнем работу.")
    return ADD_TASK  # Переход к следующему шагу

# Обработчики для шагов в ConversationHandler
async def handle_button_click(update: Update, context: CallbackContext) -> int:
    # Код обработки кнопки
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Введите название задачи:")
    return ENTER_TIME  # Переход к следующему шагу

async def handle_text(update: Update, context: CallbackContext) -> int:
    # Код для обработки введенного текста
    task_name = update.message.text
    await update.message.reply_text(f"Задача '{task_name}' добавлена.")
    return ENTER_COMMENT  # Переход к следующему шагу

# Описание шагов в ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],  # Обработчик команды /start
    states={
        ADD_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_click)],
        ENTER_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)],
        ENTER_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)],
    },
    fallbacks=[]  # Обработчик для завершения разговора (если нужен)
)