import sqlite3

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

# Добавление задачи в базу данных
def add_task_to_db(name, date, time, comment=None):
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (name, date, time, comment) VALUES (?, ?, ?, ?)', (name, date, time, comment))
    conn.commit()
    conn.close()

# Получение задач из базы данных
def get_tasks_from_db():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return tasks

# Удаление задачи из базы данных
def delete_task_from_db(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()