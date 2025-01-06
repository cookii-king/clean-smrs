# Generated by Django 5.1.4 on 2025-01-04 22:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_subscription_status_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='stripe_subscription_id',
        ),
        migrations.AddField(
            model_name='subscriptionitem',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_items', to='pages.plan', to_field='stripe_plan_id'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='subscriptionitem',
            name='price',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_items', to='pages.price', to_field='stripe_price_id'),
        ),
    ]