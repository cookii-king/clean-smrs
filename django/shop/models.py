import uuid
from django.db import models
from accounts.models import Account

class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    account_id= models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    order_date=models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)


# Product Model
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    def update_stock(self, quantity):
        # Add stock update logic here
        pass

# Cart Model
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='carts')
    created_date = models.DateTimeField(auto_now_add=True)

    def add_item(self, product):
        # Logic to add a product
        pass

    def remove_item(self, product):
        # Logic to remove a product
        pass

    def calculate_total(self):
        # Logic to calculate total price
        pass

# Subscription Model
class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    subscription_type = models.CharField(max_length=50)

    def subscribe(self):
        # Logic for subscribing
        pass

    def cancel(self):
        # Logic for cancelling
        pass