import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
from ...models import Product

class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(max_length=3)
    interval = models.CharField(max_length=255) 
    # product = models.CharField(max_length=500)
    product = models.ForeignKey(Product, to_field='stripe_product_id', on_delete=models.CASCADE, related_name='plans')
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    stripe_plan_id = models.CharField(max_length=255, blank=True, unique=True, null=True)  # Stripe product ID
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def create_or_get_stripe_plan(self):
        """
        Create or retrieve a subscription plan in Stripe.
        """
        try:
            if self.stripe_plan_id:
                # Check if the plan exists in Stripe
                stripe_plan = stripe.Plan.retrieve(self.stripe_plan_id)
                print(f"Found existing Stripe plan: {stripe_plan['id']}")
                return stripe_plan
            else:
                # Convert amount to cents (Stripe expects amounts in cents)
                amount_in_cents = int(self.amount * 100)
                # Create a new plan in Stripe
                stripe_plan = stripe.Plan.create(
                    amount=amount_in_cents,
                    currency=self.currency,
                    interval=self.interval,
                    product=self.product.stripe_product_id,
                )
                self.stripe_plan_id = stripe_plan["id"]
                self.save()
                print(f"Created new Stripe plan: {stripe_plan['id']}")
                return stripe_plan
        except Exception as e:
            print(f"Error in create_or_get_stripe_plan: {e}")
            raise

    def delete_stripe_plan(self):
        """
        Delete the Stripe plan associated with this model.
        """
        if self.stripe_plan_id:
            try:
                stripe.Plan.delete(self.stripe_plan_id)
                print(f"Deleted Stripe plan: {self.stripe_plan_id}")
                self.stripe_plan_id = None
                self.save()
            except Exception as e:
                print(f"Error deleting Stripe plan: {e}")
                raise

    def save(self, *args, **kwargs):
        """
        Override save to ensure a Stripe plan is created or linked.
        """
        if not self.stripe_plan_id:
            self.create_or_get_stripe_plan()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        Override the delete method to delete the Stripe plan first.
        """
        if self.stripe_plan_id:
            self.delete_stripe_plan()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.id)  # Convert UUID to string