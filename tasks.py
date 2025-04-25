user_tasks = {}

def create_task(user_id, task_data):
    if user_id not in user_tasks:
        user_tasks[user_id] = []

    task = {
        "name": task_data.get("task_name"),
        "date": task_data.get("task_date"),
        "time": task_data.get("task_time"),
        "reminder_minutes": task_data.get("reminder_minutes"),
        "comment": task_data.get("comment", "")
    }

    user_tasks[user_id].append(task)

def get_user_tasks(user_id):
    return user_tasks.get(user_id, [])

def get_task_by_id(user_id, index):
    return user_tasks.get(user_id, [])[index]

def delete_task(user_id, task):
    if user_id in user_tasks:
        if task in user_tasks[user_id]:
            user_tasks[user_id].remove(task)