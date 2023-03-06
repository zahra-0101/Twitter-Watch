from django.core.management.base import BaseCommand
from accounts.views import update_accounts

class Command(BaseCommand):
    help = 'Updates the accounts in the database'

    def handle(self, *args, **options):
        update_accounts()
        self.stdout.write(self.style.SUCCESS('Successfully updated the accounts'))