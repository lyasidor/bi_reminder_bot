from datetime import datetime, timedelta
from telegram import KeyboardButton, ReplyKeyboardMarkup
from timezonefinder import TimezoneFinder
import pytz

tasks = {}

def get_new_task_id():
    return max(tasks.keys(), default=0) + 1

def generate_date_keyboard():
    today = datetime.now()
    buttons = [[(today + timedelta(days=i)).strftime("%d-%m-%Y")] for i in range(5)]
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)

def get_timezone_by_location(lat, lon):
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    return pytz.timezone(tz_name) if tz_name else pytz.utc

def get_local_time(utc_dt, tz):
    return utc_dt.astimezone(tz)
