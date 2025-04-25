tasks = {}
_task_id = 0

def get_new_task_id():
    global _task_id
    _task_id += 1
    return _task_id