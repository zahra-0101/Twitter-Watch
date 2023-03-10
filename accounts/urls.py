from django.urls import path
from . import views

urlpatterns = [
    path('global_var/', views.global_var_view, name='global_var'),
    # other URL patterns here...
]