import uuid
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class Account(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    email_confirmation_secret = models.CharField(max_length=16, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=16, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def generate_email_confirmation_secret(self):
        """Generates an 8-digit numeric code for email confirmation."""
        self.email_confirmation_secret = '{:08d}'.format(random.randint(0, 99999999))
        self.save()

    def validate_email_confirmed(self):
        """Marks the email as confirmed."""
        self.email_confirmed = True
        self.save()

    def __str__(self):
        return self.username or self.email
