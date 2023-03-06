from django.urls import path
from .views import TwitterAccountList, TwitterThreadAPIView, AudienceInfoAPIView

urlpatterns = [
    path('accounts/', TwitterAccountList.as_view(), name='account_list'),
    path('tweets/<twitter_handle>/', TwitterThreadAPIView.as_view(), name='twitter_threads'),
    path('audience-info/<str:twitter_handle>/', AudienceInfoAPIView.as_view(), name='audience_info'),

]
