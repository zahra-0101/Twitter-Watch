from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from accounts.models import TwitterAccount, TwitterThread
from .serializers import TwitterAccountSerializer, TwitterThreadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# from .models import TwitterThread
class TwitterAccountList(generics.ListCreateAPIView):
    queryset = TwitterAccount.objects.all()
    serializer_class = TwitterAccountSerializer


class TwitterThreadAPIView(APIView):
    def get(self, request, twitter_handle):
        threads = TwitterThread.objects.filter(account__twitter_handle=twitter_handle)
        serializer = TwitterThreadSerializer({'account': twitter_handle, 'threads': threads})
        return Response(serializer.data)