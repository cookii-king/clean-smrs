import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
from ...models import Price, Plan
class SystemLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.id)