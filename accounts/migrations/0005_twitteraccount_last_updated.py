# Generated by Django 4.1.7 on 2023-03-07 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_twitteraccount_last_tweet_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteraccount',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
