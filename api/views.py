from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from accounts.models import TwitterAccount
from .serializers import TwitterAccountSerializer

class TwitterAccountList(generics.ListCreateAPIView):
    queryset = TwitterAccount.objects.all()
    serializer_class = TwitterAccountSerializer

