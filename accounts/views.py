from django.shortcuts import render
from accounts.models import TwitterAccount, TwitterThread
# Create your views here.
import os
import configparser
import tweepy
from datetime import datetime
import pytz
import time
from collections import Counter

utc=pytz.UTC

def authenticate(func):
    def wrapper():
        # Get the path to the config.ini file in the root directory of the Django project
        config_path = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'config.ini')

        # Read the Twitter API credentials from conf/ig.ini
        config = configparser.ConfigParser()
        config.read(config_path)
        consumer_key = config['TwitterAPI']['consumer_key']
        consumer_secret = config['TwitterAPI']['consumer_secret']
        access_token = config['TwitterAPI']['access_token']
        access_token_secret = config['TwitterAPI']['access_token_secret']
        # print ('access_token_secret', access_token_secret)
        # Authenticate with Twitter API
        # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # auth.set_access_token(access_token, access_token_secret)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        # Call the function with the authenticated API object
        func(api)
        # return api
    return wrapper

@authenticate
def update_accounts(api):
    accounts = TwitterAccount.objects.all()
    for account in accounts:
        user = api.get_user(screen_name=account.twitter_handle)

        account.display_name = user.name
        account.bio = user.description
        accounts.profile_picture = user.profile_image_url
        accounts.follower_count = user.followers_count
        account.following_count = user.friends_count
        accounts.created_at = user.created_at
        account.save()


@authenticate
def get_user_threads_since_date(api):
    """
    Extracts all threads belonging to a user starting from a specific date.
    """
    since_time = datetime(2023, 2, 1)  # set the time range as February 1st, 2023
    
    accounts = TwitterAccount.objects.all()
    for account in accounts:
    
        MAX_RETRIES = 3  # maximum number of times to retry the request
        retry_count = 0  # current number of retries

        while retry_count < MAX_RETRIES:
            try:
                tweets = []
                for tweet in tweepy.Cursor(api.user_timeline, screen_name=account.twitter_handle, tweet_mode='extended').items():
                    # print(1)
                    if tweet.created_at > utc.localize(since_time):
                        tweets.append(tweet)
                print(account.twitter_handle)
                for tweet in tweets:
                    replies = []
                    replies.append(tweet.full_text)
                    for reply in tweepy.Cursor(api.search_tweets, q='to:'+account.twitter_handle, since_id=tweet.id, tweet_mode='extended').items():
                        if hasattr(reply, 'in_reply_to_status_id_str'):
                            if reply.in_reply_to_status_id_str == tweet.id_str:
                                replies.append({
                                'author': reply.user.screen_name,
                                'text': reply.full_text,
                                'num_likes': reply.favorite_count
                            })
                            
                    new_thread = TwitterThread(
                    account=account,
                    tweet_id=tweet.id,
                    tweet_text=tweet.full_text,
                    # conversation_id=tweet.conversation_id,
                    conversation=replies,
                    created_at=datetime.now()
                    )
                    # save the instance to the database
                    new_thread.save()
                TwitterAccount.objects.filter(pk=account.id).update(
                    last_tweet_id = tweet.id)

            except tweepy.TweepyException as e:
                print("Error: Failed to send request")
                print(e)
                retry_count += 1  # increment the retry count
                time.sleep(5)
                print(account.twitter_handle)
                if e == 'Error: Failed to send request' +'\n' + '429 Too Many Requests':
                    print('sleep')
                    time.sleep(900)
                    retry_count = 0       


@authenticate
def get_user_threads_since_id(api):
    """
    Extracts all threads belonging to a user after a specific tweet id.
    """

    accounts = TwitterAccount.objects.all()
    for account in accounts:
    
        tweets = []
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=account.twitter_handle, since_id=account.last_tweet_id).items():
            tweets.append(tweet)
        print(account.twitter_handle)
        for tweet in tweets:
            replies = []
            replies.append(tweet.full_text)
            for reply in tweepy.Cursor(api.search_tweets, q='to:'+account.twitter_handle, since_id=tweet.id, tweet_mode='extended').items():
                if hasattr(reply, 'in_reply_to_status_id_str'):
                    if reply.in_reply_to_status_id_str == tweet.id_str:
                        replies.append({
                        'author': reply.user.screen_name,
                        'text': reply.full_text,
                        'num_likes': reply.favorite_count
                    })
                    
            new_thread = TwitterThread(
            account=account.id,
            tweet_id=tweet.id,
            tweet_text=tweet.full_text,
            # conversation_id=tweet.conversation_id,
            conversation=replies,
            created_at=datetime.now()
            )
            # save the instance to the database
            new_thread.save()
        TwitterAccount.objects.filter(pk=account.id).update(
            last_tweet_id = tweet.id)

        print(account.twitter_handle)
        


def get_last_200_tweets(api, twitter_handle):
    tweets = [] 
    for tweet in tweepy.Cursor(api.user_timeline, id=twitter_handle).items(5):
        tweets.append(tweet)
    return tweets


def get_all_replies_belong_to_a_tweet(api, tweet):
    replies = []
    for reply in tweepy.Cursor(api.search_tweets, q="to:" + api.get_status(tweet.id).user.screen_name, since_id=tweet.id, tweet_mode="extended").items():
        replies.append(reply) 
    return replies
     

def extract_unique_user_from_replies(replies):
    users_screen_name = []
    users_location = []
    # followers_reply = []
    for reply in replies:
        # for reply in r:
        #     print(r)
        users_screen_name.append(reply.entities['user_mentions'][0]['screen_name'])
        users_location.append(reply.entities['user_mentions'][0]['location'])
        # followers_reply.append(reply.entities['user_mentions'][0]['location'])
    return Counter(users_screen_name) , users_location


def extract_full_text_from_replies(replies):
    full_text = []
    for reply in replies:
        full_text.append(reply.entities['user_mentions'][0]['screen_name'])
    return full_text

