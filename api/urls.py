from django.urls import path
from .views import TwitterAccountList, TwitterThreadAPIView

urlpatterns = [
    path('accounts/', TwitterAccountList.as_view(), name='account_list'),
    path('tweets/<twitter_handle>/', TwitterThreadAPIView.as_view(), name='twitter_threads'),
]
