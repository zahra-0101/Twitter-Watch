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
    account_id = models.IntegerField(
        blank=False
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
    follower_count = models.IntegerField(
        null=True,
        blank=True
    )

    # Twitter account follower count
    following_count = models.IntegerField(
        null=True, 
        blank=True
    )

    # Date when the account was added to the database
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        """
        String representation of the TwitterAccount model
        """
        return self.username



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

    # Conversation ID of the thread (optional)
    conversation_id = models.CharField(
        max_length=255, 
        null=True, 
        blank=True)

    # Thread conversation (as a JSON string)
    conversation = models.TextField()

    # Date when the thread was added to the database
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the TwitterThread model
        """
        return f'{self.account.username} - Thread {self.tweet_id}'