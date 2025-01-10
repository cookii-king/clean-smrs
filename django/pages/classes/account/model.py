import uuid, pyotp, random
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from ...config.config import stripe
from system.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


class Account(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, unique=True)
    email_confirmation_secret = models.CharField(max_length=16, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=16, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)
    mfa_confirmed = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    stripe_customer_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
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

    def validate_mfa_confirmed(self):
        """Marks the mfa as confirmed."""
        self.mfa_confirmed = True
        self.save()

    def validate_mfa_unconfirmed(self):
        """Marks the mfa as confirmed."""
        self.mfa_confirmed = False
        self.save()

    def send_confirmation_email(self):
        """Send the confirmation email to the user."""
        user_name = self.name or self.username or "User"
        try:
            send_mail(
                subject=f"Please confirm your email, {user_name}",
                message=f"Your confirmation secret is: {self.email_confirmation_secret}",
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[self.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise Exception(f"Failed to send email: {e}")

    def create_stripe_customer(self):
        """Creates a Stripe customer and stores the customer ID."""
        try:
            # Create a new Stripe customer
            customer = stripe.Customer.create(
                email=self.email,
                name=self.name,
                description=f"Customer for {self.email}"
            )
            # Store the Stripe customer ID in the account
            self.stripe_customer_id = customer.id
            self.save()
            return customer
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")
            raise Exception(f"Failed to create Stripe customer: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            raise Exception(f"Failed to create Stripe customer: {e}")

    def update_stripe_customer(self, **kwargs):
        """Updates the Stripe customer with the provided details."""
        if not self.stripe_customer_id:
            raise Exception("Stripe customer ID not set for this account.")

        try:
            # Update the Stripe customer
            customer = stripe.Customer.modify(
                self.stripe_customer_id,
                **kwargs
            )
            return customer
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")
            raise Exception(f"Failed to update Stripe customer: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            raise Exception(f"Failed to update Stripe customer: {e}")
        

    def delete_stripe_customer(self):
        """Deletes the Stripe customer associated with this account."""
        if not self.stripe_customer_id:
            raise Exception("Stripe customer ID not set for this account.")

        try:
            # Delete the Stripe customer
            stripe.Customer.delete(self.stripe_customer_id)

            # Optionally, clear the stripe_customer_id field
            self.stripe_customer_id = None
            self.save()

            print("Stripe customer deleted successfully.")
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")
            raise Exception(f"Failed to delete Stripe customer: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            raise Exception(f"Failed to delete Stripe customer: {e}")


    def __str__(self):
        return self.username or self.email

    # Meta Class
    class Meta:
        db_table = "pages_account"