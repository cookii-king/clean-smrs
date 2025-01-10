import uuid, pyotp, random
from django.db import models
from ...models import Product
from django.utils.timezone import now

class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(max_length=3)
    interval = models.CharField(max_length=255) 
    product = models.ForeignKey(Product, to_field='stripe_product_id', on_delete=models.CASCADE, related_name='plans')
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    stripe_plan_id = models.CharField(max_length=255, blank=True, unique=True, null=True)  # Stripe product ID
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    # Methods
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    # Meta Class
    class Meta:
        db_table = "pages_plan"