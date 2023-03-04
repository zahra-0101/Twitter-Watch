from django.test import TestCase
from .models import TwitterAccount, TwitterThread

class TwitterThreadModelTestCase(TestCase):
    """
    Test case for the TwitterThread model
    """

    def setUp(self):
        """
        Create a new TwitterAccount object for testing
        """
        self.account = TwitterAccount.objects.create(username='test_user')

    def test_create_thread(self):
        """
        Test creating a new TwitterThread object
        """
        tweet_id = 123456789
        conversation = '{"tweets": [{"text": "Hello, world!"}]}'
        thread = TwitterThread.objects.create(account=self.account, tweet_id=tweet_id, conversation=conversation)

        self.assertEqual(thread.account, self.account)
        self.assertEqual(thread.tweet_id, tweet_id)
        self.assertEqual(thread.conversation, conversation)

    def test_optional_conversation_id(self):
        """
        Test creating a new TwitterThread object with an optional conversation_id field
        """
        tweet_id = 123456789
        conversation_id = '1234567890'
        conversation = '{"tweets": [{"text": "Hello, world!"}]}'
        thread = TwitterThread.objects.create(account=self.account, tweet_id=tweet_id, conversation_id=conversation_id, conversation=conversation)

        self.assertEqual(thread.conversation_id, conversation_id)
