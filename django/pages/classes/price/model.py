import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe

class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(max_length=3)
    product = models.CharField(max_length=500)
    unit_amount = models.IntegerField(default=0)
    recurring = models.JSONField(max_length=1024, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def create_in_stripe(self):
        """Create the price in Stripe and store the ID."""
        stripe_price = stripe.Price.create(currency=self.currency, product=self.product, unit_amount=self.unit_amount, recurring=self.recurring if self.recurring else None)
        self.stripe_price_id = stripe_price["id"]
        self.save()
        return stripe_price