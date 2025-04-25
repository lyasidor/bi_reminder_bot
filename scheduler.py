from apscheduler.schedulers.background import BackgroundScheduler

# Планировщик
scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()