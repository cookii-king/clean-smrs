import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)  # Stripe product ID
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def create_in_stripe(self):
        """Create the product in Stripe and store the ID."""
        stripe_product = stripe.Product.create(name=self.name, description=self.description or "")
        self.stripe_product_id = stripe_product["id"]
        self.save()
        return stripe_product