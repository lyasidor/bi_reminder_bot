import datetime

tasks = {}  # Здесь будут храниться задачи

def add_task(task_data):
    task_id = len(tasks) + 1
    tasks[task_id] = task_data
    return task_id

def get_task(task_id):
    return tasks.get(task_id)

def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
