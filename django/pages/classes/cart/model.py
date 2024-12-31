from django.db import model
from django.conf import settings
from product.model import Product  # Adjust this import to match your project structure

class Cart(model.Model):
    """
    Represents a shopping cart associated with a user.
    """
    user = model.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=model.CASCADE,
        related_name='cart'
    )
    created_at = model.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(model.Model):
    """
    Represents an item in the shopping cart.
    """
    cart = model.ForeignKey(Cart, on_delete=model.CASCADE, related_name='items')
    product = model.ForeignKey(Product, on_delete=model.CASCADE)
    quantity = model.PositiveIntegerField(default=1)
    added_at = model.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart of {self.cart.user.username}"

    @property
    def total_price(self):
        """
        Calculates the total price for this cart item.
        """
        return self.product.price * self.quantity
