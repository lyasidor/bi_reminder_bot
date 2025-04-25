from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from keyboards import start_markup, generate_date_keyboard, back_markup, skip_or_back_markup
from states import *
from tasks import tasks, get_new_task_id
import datetime
import re

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выбери действие:",
        reply_markup=start_markup()
    )
    return CHOOSING

async def choose_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice == "Добавить задачу":
        await update.message.reply_text("Какую задачу добавишь?", reply_markup=back_markup())
        return TASK_NAME
    elif choice == "Список задач":
        return await list_tasks(update, context)
    else:
        await update.message.reply_text("Пожалуйста, выбери действие с кнопок.")
        return CHOOSING

async def task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_name'] = update.message.text
    await update.message.reply_text("Выбери дату:", reply_markup=generate_date_keyboard())
    return DATE

async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['task_date'] = update.callback_query.data
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Напиши время в формате хх:хх (например, 18:24):", reply_markup=back_markup())
    return TIME

async def time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if re.match(r"\d{2}:\d{2}", update.message.text):
        context.user_data['task_time'] = update.message.text
        await update.message.reply_text("За сколько минут до начала напомнить?", reply_markup=back_markup())
        return REMINDER
    await update.message.reply_text("Введи корректное время в формате хх:хх", reply_markup=back_markup())
    return TIME

async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.isdigit():
        context.user_data['reminder'] = int(update.message.text)
        await update.message.reply_text("Введи комментарий к задаче или нажми 'Пропустить'", reply_markup=skip_or_back_markup())
        return COMMENT
    await update.message.reply_text("Введи число минут", reply_markup=back_markup())
    return REMINDER

async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comment = update.message.text
    if comment.lower() == "пропустить":
        comment = ""
    context.user_data['comment'] = comment

    task_id = get_new_task_id()
    tasks[task_id] = context.user_data.copy()

    await update.message.reply_text("Задача успешно создана!", reply_markup=start_markup())
    return CHOOSING

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not tasks:
        await update.message.reply_text("У тебя нет задач.", reply_markup=start_markup())
        return CHOOSING
    buttons = []
    for i, (task_id, task) in enumerate(tasks.items()):
        text = f"{task['task_name']} – {task['task_date']} {task['task_time']}"
        buttons.append(InlineKeyboardButton(text, callback_data=f"detail_{task_id}"))

    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back_to_menu")])

    await update.message.reply_text("Список задач:", reply_markup=InlineKeyboardMarkup(keyboard))
    return TASK_LIST

async def task_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_id = int(query.data.replace("detail_", ""))
    task = tasks.get(task_id)
    await query.answer()

    text = f"Название задачи: {task['task_name']}\nДата: {task['task_date']}, Время: {task['task_time']}\nКомментарий: {task['comment'] or 'нет'}"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Удалить задачу", callback_data=f"delete_{task_id}")],
        [InlineKeyboardButton("Назад", callback_data="back_to_list")]
    ])
    await query.edit_message_text(text, reply_markup=keyboard)
    return TASK_DETAILS

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_id = int(update.callback_query.data.replace("delete_", ""))
    tasks.pop(task_id, None)
    await update.callback_query.answer("Задача удалена.")
    return await list_tasks(update, context)

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Выбери действие:", reply_markup=start_markup())
    return CHOOSING

def get_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT, choose_action)],
            TASK_NAME: [MessageHandler(filters.TEXT, task_name)],
            DATE: [CallbackQueryHandler(date)],
            TIME: [MessageHandler(filters.TEXT, time)],
            REMINDER: [MessageHandler(filters.TEXT, reminder)],
            COMMENT: [MessageHandler(filters.TEXT, comment)],
            TASK_LIST: [CallbackQueryHandler(task_details, pattern="^detail_"), CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$")],
            TASK_DETAILS: [CallbackQueryHandler(delete_task, pattern="^delete_"), CallbackQueryHandler(list_tasks, pattern="^back_to_list$")],
        },
        fallbacks=[]
    )