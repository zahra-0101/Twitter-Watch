import configparser
import datetime as dt
import os
from datetime import datetime

import pytz
import snscrape.modules.twitter as sntwitter
import tweepy
from django.shortcuts import render
from django.utils import timezone
from django.db import IntegrityError

from accounts.models import TwitterAccount, TwitterThread

from .decorators import handle_rate_limit_error, authenticate

utc=pytz.UTC


@authenticate
def update_accounts(api):
    # updates Twitter accounts information.

    accounts = TwitterAccount.objects.all()
    for account in accounts:
        user = api.get_user(screen_name=account.twitter_handle)

        account.display_name = user.name
        account.bio = user.description
        accounts.profile_picture = user.profile_image_url
        accounts.follower_count = user.followers_count
        account.following_count = user.friends_count
        account.last_updated = timezone.now().time()
        account.save()

def update_account(api, account, rate_limit):
    # updates a Twitter account information.

    user = api.get_user(screen_name=account.twitter_handle)
    account.display_name = user.name
    account.bio = user.description
    account.profile_picture = user.profile_image_url
    account.follower_count = user.followers_count
    account.following_count = user.friends_count
    account.last_updated = timezone.now().time()
    account.rate_limit = rate_limit
    account.save()
 
 
# @handle_rate_limit_error
# def update_thread(api, tweet):
#     replies = []
#     # Search for replies to the tweet using the tweet ID
#     replies.append(tweet.text)
#     for reply in tweepy.Cursor(api.search, q='to:{}'.format(tweet.id), since_id=tweet.id, tweet_mode='extended').items():                   
#         if reply.in_reply_to_status_id_str == tweet.id_str:
#             replies.append({
#             'author': reply.user.screen_name,
#             'text': reply.full_text,
#             'num_likes': reply.favorite_count
#         })
#     TwitterThread.objects.filter(pk=tweet.id).update(
#                     conversation = replies,
#                     last_update = timezone.now().time()
#     )


def get_all_replies_belong_to_a_tweet(api, account, tweet):
    replies = []
    replies.append(tweet.rawContent)
    for reply in enumerate(sntwitter.TwitterSearchScraper(f'conversation_id:{tweet.conversationId} filter:safe').get_items()):
        if hasattr(reply, 'in_reply_to_status_id_str'):
            if reply.in_reply_to_status_id_str == str(tweet.id):
                replies.append({
                'author': reply.user.screen_name,
                'text': reply.full_text,
                'num_likes': reply.favorite_count
            })
    return replies


@handle_rate_limit_error
def database_initializer(api, accounts, since_time):
    start_date = since_time

    # Define the search query
    for account in accounts:
        if since_time:
            search_query = "from:{} since:{} ".format(account.twitter_handle, start_date)
        else:
            search_query = "from:{} since_id:{}".format(account.twitter_handle, account.last_tweet_id)

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):

            replies = get_all_replies_belong_to_a_tweet(api, account, tweet)
            try:
                new_thread = TwitterThread(
                account=account,
                tweet_id=tweet.id,
                tweet_text=tweet.rawContent,
                # conversation_id=tweet.conversation_id,
                conversation=replies,
                created_at=datetime.now()
                )
                # save the instance to the database
                new_thread.save()
            except IntegrityError:
                pass

            TwitterAccount.objects.filter(pk=account.id).update(
                last_tweet_id = tweet.id)
            update_account(api, account, True)
            print('database_initializer')

        update_account(api, account, False)

      
@authenticate
def update_tweets_for_user(api):
    """
    Extracts all threads belonging to a user (as long as possible) starting from a specific date.
    """

    # Create an empty list to hold the tweets
    tweets = []
    since_time = datetime(2023, 2, 1)  # set the time range as February 1st, 2023
    accounts = TwitterAccount.objects.filter(rate_limit=False).order_by('-last_updated')

    if accounts.exists():
        # initializing database
        print(accounts)
        database_initializer(api, accounts, since_time) 


@authenticate
def update_database(api):
    """
    Update Database
    """

    update_accounts(api)
    accounts = TwitterAccount.objects.filter(rate_limit=False).order_by('-last_updated')
    database_initializer(api, accounts)

