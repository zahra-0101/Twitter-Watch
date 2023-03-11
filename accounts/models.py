from django.db import models

# Create your models here.


class TwitterAccount(models.Model):
    """
    Model to store Twitter accounts
    """

    # Twitter account username
    twitter_handle = models.CharField(
        max_length=50, 
        unique=True
    )

    # Twitter account ID
    account_id = models.CharField(
        max_length=255, 
        unique=True, 
        null=True, 
        blank=True
    )

    # Twitter account display name
    display_name = models.CharField(
        max_length=100
    )

    # Twitter account bio
    bio = models.TextField(
        null=True,
        blank=True
    )

    # Twitter account profile picture
    profile_picture = models.URLField(
        null=True,
        blank=True
    )

    # Twitter account follower count
    follower_count = models.BigIntegerField(
        null=True,
        blank=True
    )

    # Twitter account follower count
    following_count = models.BigIntegerField(
        null=True, 
        blank=True
    )

    # Date when the account was added to the database
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    last_tweet_id = models.BigIntegerField(
        null=True,
        blank=True
    )
    
    twitter_url = models.URLField(blank=True, null=True)
    banner_url = models.URLField(blank=True, null=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    rate_limit = models.BooleanField(default=False)
    def __str__(self):
        """
        String representation of the TwitterAccount model
        """
        return self.twitter_handle



class TwitterThread(models.Model):
    """
    Model to store Twitter threads for a particular Twitter account
    """

    # Twitter account that the thread belongs to
    account = models.ForeignKey(
        TwitterAccount, 
        on_delete=models.CASCADE, 
        related_name='threads')

    # Thread tweet ID (the first tweet in the thread)
    tweet_id = models.BigIntegerField()

    tweet_text = models.CharField(
        max_length=1000, 
        null=True, 
        blank=True
    )

    # Conversation ID of the thread (optional)
    conversation_id = models.CharField(
        max_length=255, 
        null=True, 
        blank=True)

    # Thread conversation (as a JSON string)
    conversation = models.TextField(blank=True, null=True)

    # Date when the thread was added to the database
    created_at = models.DateTimeField(auto_now_add=True)

    last_updated = models.DateTimeField(auto_now=True)

    # Basic information
    num_tweets = models.IntegerField(null=True)  # the number of tweets in the conversation
    start_time = models.DateTimeField(null=True)  # the time when the first tweet was posted
    end_time = models.DateTimeField(null=True)  # the time when the last tweet was posted

    # Tweet-level features
    tweet_length = models.TextField(null=True)  # the length of each tweet in terms of characters
    hashtags = models.TextField(null=True)  # the hashtags used in the conversation
    mentions = models.TextField(null=True)  # the usernames mentioned in the conversation
    emojis = models.TextField(null=True)  # the emojis used in the conversation
    sentiment = models.CharField(null=True, max_length=255)  # the sentiment of each tweet (positive, negative, or neutral)
    time_stamp = models.DateTimeField(null=True)  # the time when each tweet was posted
    replies = models.IntegerField(null=True)  # the number of replies to each tweet
    retweets = models.IntegerField(null=True)  # the number of retweets for each tweet

    # User-level features
    unique_user = models.IntegerField(null=True) # the number of unique users contributed in the thread

    class Meta:
        # unique_together = ['account', 'tweet_id']
        verbose_name = "Twitter Thread"
        verbose_name_plural = "Twitter Threads"

    def __str__(self):
        return f"{self.account.username}'s Twitter Thread {self.id}"