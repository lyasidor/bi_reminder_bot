from telegram.ext import ConversationHandler

class States:
    TASK_NAME = 1
    DATE = 2
    TIME = 3
    REMINDER_MINUTES = 4
    COMMENT = 5
    TASK_VIEW = 6
    TASK_ACTION = 7