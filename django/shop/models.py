import uuid
import datetime
from django.utils.timezone import now
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
    # total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # calculate total amount from list of products
    status = models.CharField(max_length=50)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)  # The available stock for the product
    category = models.CharField(max_length=100)  # The category of the product (e.g., SMR, Data Center, etc.)
    status = models.CharField(max_length=50)  # Status of the product (e.g., 'available', 'out of stock', etc.)
    ## will add it later image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Optional image field
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    # Optional method to calculate the total price of a product depending on its quantity in a cart
    def total_price(self, quantity):
        return self.price * quantity
    

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='carts')
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def total(self):
        total_price = sum(item.total() for item in self.cartproduct_set.all())
        return total_price

class CartProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total(self):
        return self.product.price * self.quantity

class SubscriptionPlan(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

class Subscription(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    account_id= models.ForeignKey(Account, on_delete=models.CASCADE, related_name='subscriptions')
    # plan_id= models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscriptions')
    status = models.CharField(max_length=50, default='active')
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)


