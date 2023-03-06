from django.core.management.base import BaseCommand
from accounts.views import get_user_threads_since_date

class Command(BaseCommand):
    help = 'Updates the accounts in the database'

    def handle(self, *args, **options):
        get_user_threads_since_date()
        self.stdout.write(self.style.SUCCESS('Successfully updated the accounts'))