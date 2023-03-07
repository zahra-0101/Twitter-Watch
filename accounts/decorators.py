import tweepy
import time

def handle_rate_limit_error(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except tweepy.TweepError as e:
                print("Rate limit exceeded. Waiting for 15 minutes...")
                time.sleep(15 * 60)  # Wait for 15 minutes (the time period for resetting the rate limit)
    return wrapper