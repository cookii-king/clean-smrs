import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
from ...models import Product

class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(max_length=3)
    recurring = models.JSONField(max_length=1024, null=True)
    # product = models.CharField(max_length=500)
    product = models.ForeignKey(Product, to_field='stripe_product_id', on_delete=models.CASCADE, related_name='prices')
    unit_amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    stripe_price_id = models.CharField(max_length=255, blank=True, unique=True, null=True)  # Stripe product ID
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def create_or_get_stripe_price(self):
        """
        Create or retrieve a subscription price in Stripe.
        """
        try:
            if self.stripe_price_id:
                # Check if the price exists in Stripe
                stripe_price = stripe.Price.retrieve(self.stripe_price_id)
                print(f"Found existing Stripe price: {stripe_price['id']}")
                return stripe_price
            else:
                # Convert amount to cents (Stripe expects amounts in cents)
                amount_in_cents = int(self.unit_amount * 100)
                # Create a new price in Stripe
                stripe_price = stripe.Price.create(
                    unit_amount=amount_in_cents,
                    currency=self.currency,
                    recurring=self.recurring if self.recurring else None,
                    product=self.product.stripe_product_id,
                )
                self.stripe_price_id = stripe_price["id"]
                self.save()
                print(f"Created new Stripe price: {stripe_price['id']}")
                return stripe_price
        except Exception as e:
            print(f"Error in create_or_get_stripe_price: {e}")
            raise

    def delete_stripe_price(self):
        """
        Delete the Stripe price associated with this model.
        """
        if self.stripe_price_id:
            try:
                stripe.Price.delete(self.stripe_price_id)
                print(f"Deleted Stripe price: {self.stripe_price_id}")
                self.stripe_price_id = None
                self.save()
            except Exception as e:
                print(f"Error deleting Stripe price: {e}")
                raise

    def save(self, *args, **kwargs):
        """
        Override save to ensure a Stripe price is created or linked.
        """
        if not self.stripe_price_id:
            self.create_or_get_stripe_price()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        Override the delete method to delete the Stripe price first.
        """
        if self.stripe_price_id:
            self.delete_stripe_price()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.id)  # Convert UUID to string