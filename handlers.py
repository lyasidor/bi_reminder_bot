# handlers.py
from telegram import Update
from telegram.ext import CallbackContext
from keyboard import date_keyboard, time_keyboard, back_button, start_keyboard
from tasks import add_task, get_tasks, remove_task, format_task
from reminders import set_reminders
from states import ADD_TASK, CHOOSE_DATE, ENTER_TIME, ENTER_COMMENT, LIST_TASKS

def start(update: Update, context: CallbackContext):
    keyboard = start_keyboard()
    update.message.reply_text("Привет! Я помогу тебе с напоминаниями. Выбери опцию:", reply_markup=keyboard)
    return ADD_TASK

def handle_button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'add_task':
        query.edit_message_text("Введите название задачи:")
        return ADD_TASK
    elif query.data == 'list_tasks':
        tasks = get_tasks()
        if tasks:
            for task in tasks:
                query.edit_message_text(format_task(task), reply_markup=back_button())
        else:
            query.edit_message_text("Задачи не найдены.", reply_markup=back_button())
        return LIST_TASKS
    elif query.data.startswith('date_'):
        date = query.data.split('_')[1]
        context.user_data['task_date'] = date
        query.edit_message_text(f"Вы выбрали дату {date}. Теперь введите время (формат: 18:52):", reply_markup=time_keyboard())
        return ENTER_TIME
    elif query.data == 'skip_time':
        query.edit_message_text("Введите комментарий к задаче (или пропустите):", reply_markup=back_button())
        return ENTER_COMMENT

def handle_text(update: Update, context: CallbackContext):
    user_input = update.message.text
    state = context.user_data.get('state')

    if state == ADD_TASK:
        context.user_data['task_title'] = user_input
        update.message.reply_text("Выберите дату задачи:", reply_markup=date_keyboard([f"{i+1}.04.2025" for i in range(14)]))
        return CHOOSE_DATE
    elif state == ENTER_TIME:
        context.user_data['task_time'] = user_input
        update.message.reply_text("Введите комментарий к задаче (или пропустите):", reply_markup=back_button())
        return ENTER_COMMENT
    elif state == ENTER_COMMENT:
        context.user_data['task_comment'] = user_input
        add_task(
            context.user_data['task_title'],
            context.user_data['task_date'],
            context.user_data['task_time'],
            context.user_data.get('task_comment')
        )
        set_reminders(context.user_data, update.message.from_user.timezone)
        update.message.reply_text("Задача добавлена!", reply_markup=start_keyboard())
        return ADD_TASK