import json
from django.core.management.base import BaseCommand
from accounts.models import TwitterAccount
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load accounts data into the database '
    name = 'load_demo_data'

    def handle(self, *args, **options):
        TwitterAccount.objects.all().delete()
        self.stdout.write('Deleted old data from the database')

        self.stdout.write('Loading data from fixture...')
        call_command('loaddata', 'account.json')
        self.stdout.write(self.style.SUCCESS('Demo data loaded successfully.'))
