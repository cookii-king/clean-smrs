import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.CharField(max_length=500)
    items = models.JSONField() 
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def create_in_stripe(self):
        """Create the subscription in Stripe and store the ID."""
        stripe_subscription = stripe.Subscription.create(customer=self.customer, items=self.items)
        self.stripe_subscription_id = stripe_subscription["id"]
        self.save()
        return stripe_subscription