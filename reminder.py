import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz

class Reminder:
    def __init__(self, task_manager):
        self.scheduler = AsyncIOScheduler()
        self.task_manager = task_manager

    def schedule_reminders(self):
        for task in self.task_manager.get_task_list():
            # Задаём напоминания на основе времени задачи
            task_time = datetime.strptime(f"{task['date']} {task['time']}", "%d.%m.%Y %H:%M")
            task_time = pytz.timezone('Europe/Moscow').localize(task_time)

            # Пример напоминания за 1 день до события
            self.scheduler.add_job(self.send_reminder, IntervalTrigger(seconds=(task_time - datetime.now()).total_seconds()))

        self.scheduler.start()

    async def send_reminder(self):
        # Тут будет код отправки напоминания
        pass