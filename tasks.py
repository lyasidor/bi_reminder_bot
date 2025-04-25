tasks = []

# Функция добавления задачи
def add_new_task(name, date, time, comment=None):
    task = {
        "name": name,
        "date": date,
        "time": time,
        "comment": comment
    }
    tasks.append(task)

# Получить список задач
def get_task_list():
    return tasks

# Получить подробности задачи
def get_task_details(task_id):
    try:
        return tasks[int(task_id)]  # Преобразуем ID в индекс списка
    except IndexError:
        return None

# Удалить задачу
def delete_task(task_id):
    try:
        tasks.pop(int(task_id))  # Удаление задачи по индексу
    except IndexError:
        return None