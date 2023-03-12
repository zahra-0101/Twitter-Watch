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
app.conf.update(
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 43200},
    BROKER_CONNECTION_TIMEOUT=30,
    # ... other configuration values ...
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
