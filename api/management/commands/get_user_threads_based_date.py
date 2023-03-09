# This script updates tweets for all users in the database.

from django.core.management.base import BaseCommand

from accounts.views import update_tweets_for_user


class Command(BaseCommand):
    help = 'Updates the accounts in the database'

    def handle(self, *args, **options):
        update_tweets_for_user()
        self.stdout.write(self.style.SUCCESS('Successfully updated the accounts'))