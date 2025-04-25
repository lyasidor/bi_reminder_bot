from datetime import datetime
from tasks import Session, Task

# Функция для получения задачи по ID
def get_task_by_id(task_id):
    session = Session()
    task = session.query(Task).filter(Task.id == task_id).first()
    session.close()
    return task

# Функция для форматирования времени
def format_datetime(dt):
    return dt.strftime("%d-%m-%Y %H:%M")

# Функция для получения текущей даты и времени
def get_current_datetime():
    return datetime.utcnow()
