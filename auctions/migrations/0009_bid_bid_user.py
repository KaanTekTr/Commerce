# Generated by Django 3.1.7 on 2021-06-07 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_listing_in_watch'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
