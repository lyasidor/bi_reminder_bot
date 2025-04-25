from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def send_reminder(task):
    # Функция для отправки напоминания
    # Например, отправить сообщение пользователю
    pass

def schedule_reminders(task):
    # Добавление напоминания за 1 день, 12 часов и т.д.
    scheduler.add_job(send_reminder, 'date', run_date=task.date, args=[task])
    # Здесь нужно добавить напоминания для всех времени (1 день, 12 часов и так далее)


class Task:
    def __init__(self, name, date, time, comment=None):
        self.name = name
        self.date = date
        self.time = time
        self.comment = comment

task_list = []

def add_task_to_list(name, date, time, comment=None):
    task = Task(name, date, time, comment)
    task_list.append(task)
