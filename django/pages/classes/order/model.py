import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
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