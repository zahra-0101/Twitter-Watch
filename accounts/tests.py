from django.test import TestCase
from datetime import datetime
from .models import TwitterAccount, TwitterThread


class TwitterAccountTestCase(TestCase):
    def test_create_account(self):
        account = TwitterAccount.objects.create(twitter_handle='test_user', account_id='12345')

        self.assertEqual(account.twitter_handle, 'test_user')
        self.assertEqual(account.account_id, '12345')
        self.assertIsNotNone(account.created_at)
        # self.assertIsNotNone(account.updated_at)
        


class TwitterThreadTestCase(TestCase):
    def setUp(self):
        self.test_account = TwitterAccount.objects.create(twitter_handle='test_user', account_id='12345')
        self.test_thread = TwitterThread.objects.create(account=self.test_account, conversation_id='123', tweet_count=2)

    def test_create_thread(self):
        self.assertEqual(self.test_thread.account, self.test_account)
        self.assertEqual(self.test_thread.conversation_id, '123')
        self.assertEqual(self.test_thread.tweet_count, 2)
        self.assertIsInstance(self.test_thread.created_at, datetime)
        self.assertIsInstance(self.test_thread.updated_at, datetime)