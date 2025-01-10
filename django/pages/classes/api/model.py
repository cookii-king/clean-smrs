import uuid, secrets
from django.utils.timezone import now, timedelta
from django.db import models
from ...models import Account
class ApiKey(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="api_keys")
    key = models.CharField(max_length=50, unique=True, default=secrets.token_urlsafe)
    active = models.BooleanField(default=True)
    revealed = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)
    credit_limit = models.PositiveIntegerField(default=1000)
    credits_used = models.PositiveIntegerField(default=0)
    reset_date = models.DateTimeField(default=now)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def generate_key(self):
        self.key = secrets.token_urlsafe()
        self.save()


    def regenerate_key(self):
        """Generate a new key and save it."""
        self.key = secrets.token_urlsafe()
        self.revealed = False
        self.save()
        return self.key

    def reset_credits(self):
        """Resets the credit usage for the new billing cycle."""
        self.credits_used = 0
        self.reset_date = now() + timedelta(days=30)
        self.save()

    def reveal(self):
        """Reveal the API key and mark it as revealed."""
        if not self.revealed:
            self.revealed = True
            self.save()
        return self.key if self.revealed else None
    
    def set_as_primary(self):
        """Set this key as primary and unset others."""
        ApiKey.objects.filter(account=self.account).update(primary=False)
        self.primary = True
        self.save()

    def __str__(self):
        return str(self.id)

    # Meta Class
    class Meta:
        db_table = "pages_api_key"
