tasks = []  # Здесь будут храниться все задачи

def add_task(task):
    tasks.append(task)

def get_tasks():
    return tasks

def delete_task(task_index):
    del tasks[task_index]