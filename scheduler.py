from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import datetime

# Инициализация планировщика
scheduler = AsyncIOScheduler()

# Функция для напоминания
def send_reminder(task_id):
    # Заменить на логику отправки напоминания пользователю
    print(f"Напоминание о задаче {task_id}!")

# Функция для планирования напоминания
def schedule_reminder(task_time, task_id):
    scheduler.add_job(send_reminder, DateTrigger(run_date=task_time), args=[task_id])

# Запуск планировщика
scheduler.start()
