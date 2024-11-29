import uuid
from django.db import models
from accounts.models import Account

class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    account_id= models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    order_date=models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
