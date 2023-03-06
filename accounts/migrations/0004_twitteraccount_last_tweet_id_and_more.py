# Generated by Django 4.1.7 on 2023-03-05 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_twitterthread_options_twitterthread_emojis_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteraccount',
            name='last_tweet_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='twitterthread',
            name='tweet_text',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='twitterthread',
            name='unique_user',
            field=models.IntegerField(null=True),
        ),
    ]