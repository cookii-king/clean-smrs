# Generated by Django 5.1.4 on 2025-01-08 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_alter_account_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='mfa_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
