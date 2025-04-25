from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from tasks import tasks
from telegram import Bot
from datetime import timedelta
from config import BOT_TOKEN
import asyncio

bot = Bot(BOT_TOKEN)
scheduler = AsyncIOScheduler()

def plan_reminder(task_id):
    task = tasks[task_id]
    trigger_time = task['task_datetime'] - timedelta(minutes=task['reminder_time'])

    async def send():
        msg = f"🔔 Напоминание о задаче:\n{task['task_name']} в {task['task_datetime'].strftime('%d-%m-%Y %H:%M')}"
        if task.get('task_comment'):
            msg += f"\n💬 {task['task_comment']}"
        await bot.send_message(task['user_id'], msg)

    scheduler.add_job(lambda: asyncio.create_task(send()), trigger=DateTrigger(run_date=trigger_time))
