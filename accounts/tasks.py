from TwitterWatch.celery import app   

from celery import shared_task
from django.conf import settings
from time import sleep

from views import update_database
@shared_task
def increment_global_var():
    # Access the global variable
    global_var = settings.MY_GLOBAL_VAR
    
    # Increment the global variable
    global_var += 1
    
    # Update the global variable
    settings.MY_GLOBAL_VAR = global_var
    
    # Wait for 15 seconds before running the task again
    sleep(15*60)
    update_database()
    # Call the task again
    increment_global_var.delay()