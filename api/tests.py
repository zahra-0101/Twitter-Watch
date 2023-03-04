from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import TwitterAccount

class TwitterAccountListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('account_list')

        self.test_account1 = TwitterAccount.objects.create(twitter_handle='test_user1')
        self.test_account2 = TwitterAccount.objects.create(twitter_handle='test_user2')

    def test_account_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        account1 = response.data[0]
        self.assertEqual(account1['id'], self.test_account1.id)
        self.assertEqual(account1['twitter_handle'], self.test_account1.twitter_handle)
        self.assertEqual(account1['account_id'], self.test_account1.account_id)

        account2 = response.data[1]
        self.assertEqual(account2['id'], self.test_account2.id)
        self.assertEqual(account2['twitter_handle'], self.test_account2.twitter_handle)
        self.assertEqual(account2['account_id'], self.test_account2.account_id)

    def test_account_list_create(self):
        data = {'twitter_handle': 'test_user3', 'account_id': '123456'}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TwitterAccount.objects.count(), 3)

        account = TwitterAccount.objects.get(id=response.data['id'])
        self.assertEqual(account.twitter_handle, 'test_user3')
        self.assertEqual(account.account_id, '123456')

