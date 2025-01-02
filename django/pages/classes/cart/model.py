# django/pages/classes/cart/model.py

from django.db import models
from pages.classes.account.model import Account
from pages.classes.product.model import Product

class Cart(models.Model):
    """
    Represents a user's shopping cart.
    Each user can have only one cart.
    """
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="cart")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    """
    Represents an item in the shopping cart.
    A cart can have many cart items, each pointing to a product.
    """
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} in cart for {self.cart.user.username}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
