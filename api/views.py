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
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon if it is not already installed
nltk.download('vader_lexicon')

def sentiment_analyzer(text):

    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    return sentiment_score['compound']


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

        # sentiment_polarity = sentiment_analyzer(' '.join(replies))
        sentiment_polarity = None
        # Serialize the audience information and return it as a response
        audience_info = {
            'followers_count': followers_count,
            'following_count': following_count,
            'followers_to_following_rate': followers_count/following_count,
            'avg_likeCount': avg_likeCount,
            'avg_quoteCount': avg_quoteCount,
            'avg_replyCount': avg_replyCount,
            'audience_sentiment_polarity': sentiment_polarity
            
        }
        serializer = AudienceInfoSerializer(audience_info)
        return Response(serializer.data)


class SentimentAPIView(generics.GenericAPIView ):
    serializer_class = AudienceInfoSerializer

    def get(self, request, twitter_handle, format=None):
        # Authenticate with the Twitter API
        config_path = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'config.ini')

        # Read the Twitter API credentials from conf/ig.ini
        config = configparser.ConfigParser()
        config.read(config_path)
        consumer_key = config['TwitterAPI']['consumer_key']
        consumer_secret = config['TwitterAPI']['consumer_secret']
        access_token = config['TwitterAPI']['access_token']
        access_token_secret = config['TwitterAPI']['access_token_secret']

        # Authenticate with Twitter API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        user = api.get_user(screen_name=twitter_handle)

        # Retrieve the audience information for the user
        followers_count = user.followers_count
        following_count = user.friends_count
        tweet_count = user.statuses_count
        created_at = user.created_at
        #TODO  hashtag

        # Serialize the audience information and return it as a response
        audience_info = {
            'followers_count': followers_count,
            'following_count': following_count,
            'tweet_count': tweet_count,
            'created_at': created_at,
        }
        serializer = AudienceInfoSerializer(audience_info)
        return Response(serializer.data)