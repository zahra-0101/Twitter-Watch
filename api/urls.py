from django.urls import path
from .views import TwitterAccountList

urlpatterns = [
    path('accounts/', TwitterAccountList.as_view(), name='account_list'),
]
