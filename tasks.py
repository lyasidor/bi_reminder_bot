from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    reminder_time = Column(Integer, nullable=False)  # В минутах
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Создаем подключение к базе данных
engine = create_engine('sqlite:///tasks.db')  # Поменяйте на вашу строку подключения
Session = sessionmaker(bind=engine)
session = Session()

# Создание таблиц (если они еще не созданы)
Base.metadata.create_all(engine)

def add_task_to_db(task_name, due_date, reminder_time):
    new_task = Task(name=task_name, due_date=due_date, reminder_time=reminder_time)
    session.add(new_task)
    session.commit()
    return new_task

def get_all_tasks():
    return session.query(Task).all()