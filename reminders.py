from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import pytz

scheduler = BackgroundScheduler()

def set_reminders(task, user_timezone):
    # Преобразуем время задачи в UTC
    task_time = datetime.strptime(f"{task['date']} {task['time']}", "%d.%m.%Y %H:%M")
    task_time = pytz.timezone(user_timezone).localize(task_time)

    # Напоминания за 1 день, 12 часов, 6 часов, 2 часа, 1 час, 30 минут, 15 минут
    reminders = [
        ("1 день", task_time - timedelta(days=1)),
        ("12 часов", task_time - timedelta(hours=12)),
        ("6 часов", task_time - timedelta(hours=6)),
        ("2 часа", task_time - timedelta(hours=2)),
        ("1 час", task_time - timedelta(hours=1)),
        ("30 минут", task_time - timedelta(minutes=30)),
        ("15 минут", task_time - timedelta(minutes=15)),
    ]

    for reminder in reminders:
        scheduler.add_job(
            send_reminder,
            'date',
            run_date=reminder[1],
            args=[task],
            id=f"reminder_{task['title']}_{reminder[0]}"
        )
    scheduler.start()

def send_reminder(task):
    # Логика отправки напоминания пользователю
    print(f"Напоминание: {task['title']} в {task['date']} {task['time']}")
