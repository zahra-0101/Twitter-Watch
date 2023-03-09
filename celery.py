# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# from celery.schedules import crontab

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')


# app = Celery('TwitterWatch')

# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()

# # Define a periodic task that runs every 15 minutes.
# app.conf.beat_schedule = {
#     'run-task-one-every-15-minutes': {
#         'task': 'accounts.tasks.get_user_threads_since_id_task',
#         'schedule': crontab(minute='*/60')
#     },
# }