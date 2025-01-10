import uuid, pyotp, random
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from ...config.config import stripe
from system.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

from ...models import Account, Price, Plan, Product, Checkout

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Account, to_field='stripe_customer_id', on_delete=models.CASCADE)
    checkout = models.ForeignKey(
        Checkout, 
        to_field='stripe_checkout_id', 
        on_delete=models.CASCADE, 
        related_name='order_items',
        null=True
    )
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.id)

    # Meta Class
    class Meta:
        db_table = "pages_order"

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, 
        to_field='stripe_product_id', 
        on_delete=models.CASCADE, 
        related_name='order_items',
        null=True
    )
    price = models.ForeignKey(
        Price, 
        to_field='stripe_price_id', 
        on_delete=models.CASCADE, 
        related_name='order_items',
        null=True
    )
    plan = models.ForeignKey(
        Plan, 
        to_field='stripe_plan_id', 
        on_delete=models.CASCADE, 
        related_name='order_items',
        null=True
    )
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)

    # Meta Class
    class Meta:
        db_table = "pages_order_item"