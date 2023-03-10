# Generated by Django 4.1.7 on 2023-03-07 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_twitteraccount_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterthread',
            name='conversation',
            field=models.TextField(blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='twitterthread',
            unique_together={('account', 'tweet_id')},
        ),
    ]
