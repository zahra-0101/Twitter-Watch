from django.shortcuts import render
from accounts.models import TwitterAccount
# Create your views here.
import os
import configparser
import tweepy


def authenticate(func):
    def wrapper():
        # Get the path to the config.ini file in the root directory of the Django project
        config_path = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'config.ini')

        # Read the Twitter API credentials from config.ini
        config = configparser.ConfigParser()
        config.read(config_path)
        consumer_key = config['TwitterAPI']['consumer_key']
        consumer_secret = config['TwitterAPI']['consumer_secret']
        access_token = config['TwitterAPI']['access_token']
        access_token_secret = config['TwitterAPI']['access_token_secret']

        # Authenticate with Twitter API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Call the function with the authenticated API object
        func(api)
    return wrapper


@authenticate
def update_accounts(api):
    accounts = TwitterAccount.objects.all()
    for account in accounts:

        user = api.get_user(account.twitter_handle)

        account.display_name = user.name
        account.bio = user.description
        accounts.profile_picture = user.profile_image_url
        accounts.follower_count = user.followers_count
        account.following_count = user.following_count
        accounts.created_at = user.created_at
        account.save()
