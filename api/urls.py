from django.urls import path
from .views import TwitterAccountList, TwitterThreadAPIView, AudienceInfoAPIView, SentimentAPIView

urlpatterns = [
    path('accounts/', TwitterAccountList.as_view(), name='account_list'),
    path('tweets/<twitter_handle>/', TwitterThreadAPIView.as_view(), name='twitter_threads'),
    path('audience-info/<str:twitter_handle>/', AudienceInfoAPIView.as_view(), name='audience_info'),
    path('sentiment/<str:twitter_handle>/', SentimentAPIView.as_view(), name='sentiment'),

]
