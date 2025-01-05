import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
from django.conf import settings
from ...models import Account, Product

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # customer = models.ForeignKey(Account, to_field='stripe_customer_id', on_delete=models.CASCADE, )
    user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='cart'
    )
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def add_item(self, product_id, quantity=1):
        """
        Add a product to the cart or update its quantity if it already exists.
        """
        product = Product.objects.get(id=product_id)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # Update the quantity if the item already exists
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    def update_item_quantity(self, product_id, quantity):
        """
        Update the quantity of a specific product in the cart.
        """
        cart_item = self.cart_items.filter(product__id=product_id).first()
        if not cart_item:
            raise ValueError("Cart item does not exist.")

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        return cart_item

    def remove_item(self, product_id):
        """
        Remove a product from the cart.
        """
        cart_item = self.cart_items.filter(product__id=product_id).first()
        if cart_item:
            cart_item.delete()
        else:
            raise ValueError("Cart item does not exist.")

    def clear_cart(self):
        """
        Remove all items from the cart.
        """
        self.cart_items.all().delete()

    def __str__(self):
        return str(self.id)

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='cart_items'
    )
    product = models.ForeignKey(Product, to_field='stripe_product_id', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def update_quantity(self, quantity):
        """
        Update the quantity of this cart item.
        """
        if quantity > 0:
            self.quantity = quantity
            self.save()
        else:
            self.delete()

    def remove(self):
        """
        Remove this item from the cart.
        """
        self.delete()
    
    def __str__(self):
        return str(self.id)
