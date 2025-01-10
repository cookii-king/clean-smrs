# Generated by Django 5.1.4 on 2025-01-10 11:39

import django.db.models.deletion
import django.utils.timezone
import secrets
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('good', 'Good'), ('service', 'Service')], default='good', max_length=255)),
                ('reoccurrence', models.CharField(choices=[('one-time', 'One Time'), ('reoccurring', 'Re-Occurring')], default='one-time', max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('stripe_product_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'pages_product',
            },
        ),
        migrations.AddField(
            model_name='account',
            name='mfa_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(default=secrets.token_urlsafe, max_length=50, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('revealed', models.BooleanField(default=False)),
                ('primary', models.BooleanField(default=False)),
                ('credit_limit', models.PositiveIntegerField(default=1000)),
                ('credits_used', models.PositiveIntegerField(default=0)),
                ('reset_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_keys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pages_api_key',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, to_field='stripe_customer_id')),
            ],
            options={
                'db_table': 'pages_cart',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('currency', models.CharField(max_length=3)),
                ('recurring', models.JSONField(max_length=1024, null=True)),
                ('unit_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('stripe_price_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='pages.product', to_field='stripe_product_id')),
            ],
            options={
                'db_table': 'pages_price',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='pages.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.product', to_field='stripe_product_id')),
            ],
            options={
                'db_table': 'pages_cart_item',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/images/')),
                ('image_url', models.URLField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pages.product')),
            ],
            options={
                'db_table': 'pages_product_image',
            },
        ),
        migrations.CreateModel(
            name='ProductVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='product/videos/')),
                ('video_url', models.URLField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='pages.product')),
            ],
            options={
                'db_table': 'pages_product_video',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('incomplete', 'incomplete'), ('incomplete_expired', 'incomplete_expired'), ('trialing', 'trialing'), ('active', 'active'), ('past_due', 'past_due'), ('canceled', 'canceled'), ('unpaid', 'unpaid'), ('paused', 'paused')], default=None, max_length=255)),
                ('stripe_subscription_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL, to_field='stripe_customer_id')),
            ],
            options={
                'db_table': 'pages_subscription',
            },
        ),
    ]