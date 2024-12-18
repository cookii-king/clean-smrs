import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe

class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(max_length=3)
    interval = models.CharField(max_length=255)
    product = models.CharField(max_length=500)
    amount = models.IntegerField(default=0)
    stripe_plan_id = models.CharField(max_length=255, blank=True, null=True)  # Stripe product ID
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)  # Convert UUID to string


    def create_in_stripe(self):
        """Create the plan in Stripe and store the ID."""
        stripe_plan = stripe.Plan.create(currency=self.currency, interval=self.interval, product=self.product, amount=self.amount)
        self.stripe_plan_id = stripe_plan["id"]
        self.save()
        return stripe_plan