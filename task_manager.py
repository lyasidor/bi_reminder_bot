from datetime import datetime, timedelta
import pytz

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_data):
        task = {
            'name': task_data['task_name'],
            'date': task_data['task_date'],
            'time': task_data['task_time'],
            'comment': task_data.get('task_comment', None)
        }
        self.tasks.append(task)

    def get_task_list(self):
        return self.tasks

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]