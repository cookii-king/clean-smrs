import uuid
import pyotp
import random
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from ...config.config import stripe

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
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def generate_email_confirmation_secret(self):
        """Generates an 8-digit numeric code for email confirmation."""
        self.email_confirmation_secret = '{:08d}'.format(random.randint(0, 99999999))
        self.save()
    
    def generate_mfa_secret_secret(self):
        """Generates mfa secret"""
        self.mfa_secret = pyotp.random_base32()
        self.save()


    def validate_email_confirmed(self):
        """Marks the email as confirmed."""
        self.email_confirmed = True
        self.save()
    
    def validate_mfa_enabled(self):
        """Marks the mfa as enabled."""
        self.mfa_enabled = True
        self.save()

    def disable_mfa_enabled(self):
        """Marks the mfa as disabled."""
        self.mfa_enabled = False
        self.save()

    def __str__(self):
        return self.username or self.email
    
    def create_in_stripe(self):
        """Create the customer in Stripe and store the ID."""
        stripe_customer = stripe.Customer.create(email=self.email)
        self.stripe_customer_id = stripe_customer["id"]
        self.save()
        return stripe_customer