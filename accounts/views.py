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
import statistics
import json

utc=pytz.UTC


@authenticate
def update_accounts(api):
    # updates Twitter accounts information.

    accounts = TwitterAccount.objects.all()
    for account in accounts:
        for i, user in enumerate(sntwitter.TwitterSearchScraper("from:{}".format(account.twitter_handle)).get_items()):

            account.display_name = user.user.displayname
            account.bio = user.user.renderedDescription
            accounts.profile_picture = user.user.profileImageUrl
            accounts.follower_count = user.user.followersCount
            account.following_count = user.user.friendsCount
            account.last_updated = timezone.now().time()
            account.twitter_url = user.url
            account.banner_url = user.user.profileBannerUrl
            account.save()
            break


def update_account(api, account, rate_limit):
    # updates a Twitter account information.

    for i, user in enumerate(sntwitter.TwitterSearchScraper("from:{}".format(account.twitter_handle)).get_items()):
        account.display_name = user.user.displayname
        account.bio = user.user.renderedDescription
        account.profile_picture = user.user.profileImageUrl
        account.follower_count = user.user.followersCount
        account.following_count = user.user.friendsCount
        account.last_updated = timezone.now().time()
        account.rate_limit = rate_limit
        account.twitter_url = user.url
        account.save()
        break
 
 
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
    for i, reply in enumerate(sntwitter.TwitterSearchScraper(f'conversation_id:{tweet.conversationId} filter:safe').get_items()):
       
        replies.append({
            'author': reply.user.username,
            'text': reply.rawContent,
            'num_likes': reply.likeCount,
            'followersCount': reply.user.followersCount,
            'favouritesCount': reply.user.favouritesCount,
            'friendsCount': reply.user.friendsCount
        })
    return replies


def get_all_replies_belong_to_the_last_n_tweets(twitter_handle, num_tweets):

    tweets = []
    replies = []
    avg_likeCount = []
    avg_quoteCount = [] 
    avg_replyCount = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("from:{}".format(twitter_handle)).get_items()):
        if len(tweets) == num_tweets:
            break
        avg_likeCount.append(tweet.likeCount)
        avg_quoteCount.append(tweet.quoteCount)
        avg_replyCount.append(tweet.replyCount)
        tweets.append(tweet)
        for i, reply in enumerate(sntwitter.TwitterSearchScraper(f'conversation_id:{tweet.conversationId} filter:safe').get_items()):
            replies.append(reply.rawContent)

    return replies, statistics.mean(avg_likeCount), statistics.mean(avg_quoteCount), statistics.mean(avg_replyCount)


@handle_rate_limit_error
def database_initializer(api, accounts, since_time):
    start_date = dt.date(2023, 2, 1)  # set the time range as February 1st, 2023
    end_date = dt.date.today()

    # Define the search query
    for account in accounts:
        if since_time:
            search_query = "from:{} since:{} until:{}".format(account.twitter_handle, start_date, end_date)
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
                TwitterAccount.objects.filter(pk=account.id).update(
                    last_tweet_id = tweet.id)
                update_account(api, account, True)
                print('database_initializer')
            except IntegrityError:
                pass


        update_account(api, account, False)

      
@authenticate
def update_tweets_for_user(api):
    """
    Extracts all threads belonging to a user (as long as possible) starting from a specific date.
    """

    # Create an empty list to hold the tweets
    tweets = []
    since_time = dt.date(2023, 2, 1)  # set the time range as February 1st, 2023
    accounts = TwitterAccount.objects.all()

    if accounts.exists():
        # initializing database
        print(accounts)
        database_initializer(api, accounts, True) 


@authenticate
def update_database(api):
    """
    Update Database
    """

    update_accounts()
    accounts = TwitterAccount.objects.all().order_by('-last_updated')
    database_initializer(api, accounts, False)


from django.http import HttpResponse
from django.conf import settings

def global_var_view(request):
    # Access the global variable
    global_var = settings.MY_GLOBAL_VAR
    
    # Return the value of the global variable as a plain text response
    return HttpResponse(str(global_var))

