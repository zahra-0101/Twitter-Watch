# Generated by Django 4.1.7 on 2023-03-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_twitteraccount_banner_url_twitteraccount_twitter_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterthread',
            name='conversation',
            field=models.JSONField(blank=True, null=True),
        ),
    ]