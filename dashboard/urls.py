from django.urls import path
from .views import AccountList


urlpatterns = [
    path('', AccountList.as_view(), name='accounts_list'),

]
