from datetime import datetime

tasks = []

def add_task(title, date, time, comment=None):
    task = {
        "title": title,
        "date": date,
        "time": time,
        "comment": comment,
        "created_at": datetime.now()
    }
    tasks.append(task)

def get_tasks():
    return tasks

def remove_task(task):
    tasks.remove(task)

def format_task(task):
    return f"{task['title']} 📅 {task['date']} 🕒 {task['time']}"
