# celery.py
import os
from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TwitterWatch.settings')

app = Celery('TwitterWatch')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# define a periodic task to print the text every 1 minute
@app.task
def print_text():
    print("this is a test")

app.conf.beat_schedule = {
    'print-text-every-1-minute': {
        'task': 'myproject.tasks.print_text',
        'schedule': crontab(minute='*/1'),
    },
}