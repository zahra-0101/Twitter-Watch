import configparser
import os

import tweepy
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import TwitterAccount, TwitterThread

from .serializers import (AudienceInfoSerializer, TwitterAccountSerializer,
                          TwitterThreadSerializer)

import snscrape.modules.twitter as sntwitter
from accounts.views import get_all_replies_belong_to_the_last_n_tweets
from textblob import TextBlob

# Download the VADER lexicon if it is not already installed

def sentiment_analyzer(text):

    blob = TextBlob(text)
    sentiment_score = blob.sentiment
    return sentiment_score


class TwitterAccountList(generics.ListCreateAPIView):
    queryset = TwitterAccount.objects.all()
    serializer_class = TwitterAccountSerializer


class TwitterThreadAPIView(APIView):
    def get(self, request, twitter_handle):
        # Retrieve all TwitterThread objects associated with the twitter_handle parameter
        threads = TwitterThread.objects.filter(account__twitter_handle=twitter_handle)
        
        # Serialize the threads data using the TwitterThreadSerializer
        serializer = TwitterThreadSerializer({'account': twitter_handle, 'threads': threads})

        # Return the serialized data as a HTTP response
        return Response(serializer.data)


class AudienceInfoAPIView(generics.GenericAPIView ):
    serializer_class = AudienceInfoSerializer

    def get(self, request, twitter_handle, format=None):

        for i, user in enumerate(sntwitter.TwitterSearchScraper("from:{}".format(twitter_handle)).get_items()):
            # Retrieve the audience information for the user
            followers_count = user.user.followersCount
            following_count = user.user.friendsCount
            break

        replies, avg_likeCount, avg_quoteCount, avg_replyCount = get_all_replies_belong_to_the_last_n_tweets(twitter_handle, 5)

        sentiment_polarity = sentiment_analyzer(' '.join(replies))

        # Serialize the audience information and return it as a response
        audience_info = {
            'followers_count': followers_count,
            'following_count': following_count,
            'followers_to_following_rate': followers_count/following_count,
            'avg_likeCount': avg_likeCount,
            'avg_quoteCount': avg_quoteCount,
            'avg_replyCount': avg_replyCount,
            'audience_sentiment_polarity': sentiment_polarity.polarity,
            'audience_sentiment_subjectivity': sentiment_polarity.subjectivity,
            
        }
        serializer = AudienceInfoSerializer(audience_info)
        return Response(serializer.data)


class SentimentAPIView(generics.GenericAPIView ):
    serializer_class = AudienceInfoSerializer

    def get(self, request, twitter_handle, format=None):
        
        for i, user in enumerate(sntwitter.TwitterSearchScraper("from:{}".format(twitter_handle)).get_items()):
            # Retrieve the audience information for the user
            followers_count = user.user.followersCount
            following_count = user.user.friendsCount
            verified = user.user.verified
            viewCount = user.viewCount
            break

        thread_level = 0
        audience_level = 0 
    

        # Serialize the audience information and return it as a response
        audience_info = {
            'followers_count': followers_count,
            'following_count': following_count,
            'verified': verified,
            'viewCount': viewCount,
            
        }
        serializer = AudienceInfoSerializer(audience_info)
        return Response(serializer.data)