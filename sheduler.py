from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
import asyncio
from telegram import Bot
from utils import get_task_by_id  # Функция для получения задачи из базы данных по ID

scheduler = AsyncIOScheduler()

# Функция для добавления напоминания в расписание
def add_reminder(task_id, reminder_time, bot: Bot):
    task = get_task_by_id(task_id)
    if task:
        reminder_datetime = task.due_date - timedelta(minutes=reminder_time)
        scheduler.add_job(
            send_reminder,
            DateTrigger(reminder_datetime),
            args=[task, bot]
        )
        scheduler.start()

# Функция для отправки напоминания пользователю
async def send_reminder(task, bot: Bot):
    user_id = task.user_id
    message = f"Напоминание: {task.name}, время выполнения: {task.due_date}"
    await bot.send_message(user_id, message)

# Функция для проверки и корректировки времени напоминания
def validate_reminder_time(task_time):
    if task_time < 0:
        raise ValueError("Время напоминания не может быть меньше нуля.")
    return task_time
