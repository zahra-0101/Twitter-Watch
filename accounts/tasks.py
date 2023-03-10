from TwitterWatch.celery import app

# @app.task
# def print_text():
#     app.send_task('myproject.tasks.print_text')
    

# from celery import shared_task
# from .globals import MY_GLOBAL_PARAM

# @shared_task
# def increment_global():
#     MY_GLOBAL_PARAM += 1
    

from celery import shared_task
from django.conf import settings
from time import sleep

@shared_task
def increment_global_var():
    # Access the global variable
    global_var = settings.MY_GLOBAL_VAR
    
    # Increment the global variable
    global_var += 1
    
    # Update the global variable
    settings.MY_GLOBAL_VAR = global_var
    
    # Wait for 15 seconds before running the task again
    sleep(15)
    
    # Call the task again
    increment_global_var.delay()