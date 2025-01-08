import uuid
import pyotp
import random
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from ...config.config import stripe
from pages.validators import *
from django.core.mail import send_mail


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
    mfa_confirmed = models.BooleanField(default=False)
    mfa_enabled = models.BooleanField(default=False)
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

    def generate_temporary_password(self):
        """Generate a temporary password."""
        return pyotp.random_base32()[:8]  # Generate an 8-character alphanumeric password

    def send_temporary_password_email(self, temp_password):
        """Send an email with the temporary password to the user."""
        subject = "Welcome to Our Service - Temporary Password"
        message = (
            f"Hello {self.name},\n\n"
            f"Welcome to our service! Please use the following temporary password to log in:\n\n"
            f"{temp_password}\n\n"
            "We recommend changing your password after logging in.\n\n"
            "Thank you,\n"
            "The Team"
        )
        from_email = "no-reply@example.com"  # Replace with your sender email
        recipient_list = [self.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
            print(f"Temporary password email sent to {self.email}")
        except Exception as e:
            print(f"Error sending email: {e}")
            raise

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

    def validate_mfa_enabled(self):
        """Marks the mfa as enabled."""
        self.mfa_enabled = True
        self.save()

    def disable_mfa_enabled(self):
        """Marks the mfa as disabled."""
        self.mfa_enabled = False
        self.save()

    # def create_or_get_stripe_customer(self):
    #     """Get an existing Stripe customer by email or create a new one."""
    #     try:
    #         # Check if a customer with this email already exists
    #         customers = stripe.Customer.list(email=self.email).data
    #         if customers:
    #             print(f"Found existing Stripe customer for email: {self.email}")
    #             return customers[0]
    #         else:
    #             # Create a new Stripe customer
    #             stripe_customer = stripe.Customer.create(email=self.email)
    #             print(f"Created new Stripe customer for email: {self.email}")
    #             return stripe_customer
    #     except Exception as e:
    #         print(f"Error in create_or_get_stripe_customer: {e}")
    #         raise

    def create_or_get_stripe_customer(self):
        """Get an existing Stripe customer or create a new one."""
        try:
            if self.stripe_customer_id:
                stripe_customer = stripe.Customer.retrieve(self.stripe_customer_id)
                print(f"Found existing Stripe customer with ID: {self.stripe_customer_id}")
                return stripe_customer
            else:
                # Create the Stripe customer
                stripe_customer = stripe.Customer.create(
                    name=self.name,
                    email=self.email,
                    description=self.description or None,
                )
                self.stripe_customer_id = stripe_customer["id"]
                self.save()
                print(f"Created new Stripe customer with ID: {stripe_customer['id']}")
                return stripe_customer
        except Exception as e:
            print(f"Error in create_or_get_stripe_customer: {e}")
            raise

    def update_stripe_customer(self):
        """Update the Stripe customer with the latest account details."""
        if self.stripe_customer_id:
            try:
                stripe.Customer.modify(
                    self.stripe_customer_id,
                    email=self.email,
                    name=self.name,
                )
                print(f"Updated Stripe customer: {self.stripe_customer_id}")
            except Exception as e:
                print(f"Error updating Stripe customer: {e}")

    def delete_stripe_customer(self):
        """Delete the Stripe customer associated with this account."""
        if self.stripe_customer_id:
            try:
                stripe.Customer.delete(self.stripe_customer_id)
                self.stripe_customer_id = None
                self.save()
                print(f"Deleted Stripe customer: {self.stripe_customer_id}")
            except Exception as e:
                print(f"Error deleting Stripe customer: {e}")

    def save(self, *args, **kwargs):
        # Validate email
        CustomEmailValidator().validate(self.email)

        # Generate and hash a temporary password if no password is provided
        if not self.password:
            temp_password = self.generate_temporary_password()
            self.password = make_password(temp_password)
            self.send_temporary_password_email(temp_password)

        # Ensure a Stripe customer is created or linked
        if not self.stripe_customer_id:
            self.create_or_get_stripe_customer()

        # Hash the password if it's not already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            CustomPasswordValidator().validate(self.password)
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        """Handle soft delete and remove Stripe customer."""
        if self.is_superuser:
            # Check if this is the last admin
            if Account.objects.filter(is_superuser=True).count() == 1:
                raise ValueError("Cannot delete the last admin account.")
        if self.is_superuser is False:
            # Check if this is the last admin
            if Account.objects.filter(is_superuser=True).count() == 1 and self.pk == Account.objects.get(is_superuser=True).pk:
                raise ValueError("Cannot remove admin privileges from the last admin account.")
        self.deleted = now()
        self.save()
        if self.stripe_customer_id:
            self.delete_stripe_customer()
        

    def __str__(self):
        return self.username or self.email

# import uuid
# import pyotp
# import random
# from django.db import models
# from django.utils.timezone import now
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import AbstractUser
# from ...config.config import stripe
# from pages.validators import CustomEmailValidator, CustomPasswordValidator

# class Account(AbstractUser):
#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False,
#     )
#     username = models.CharField(max_length=255, unique=True, null=True, blank=True)
#     name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255, unique=True)
#     email_confirmation_secret = models.CharField(max_length=16, blank=True, null=True)
#     email_confirmed = models.BooleanField(default=False)
#     mfa_secret = models.CharField(max_length=16, blank=True, null=True)
#     mfa_enabled = models.BooleanField(default=False)
#     password = models.CharField(max_length=255)
#     stripe_customer_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
#     created = models.DateTimeField(default=now)
#     updated = models.DateTimeField(auto_now=True)
#     deleted = models.DateTimeField(null=True, blank=True)

#     def generate_email_confirmation_secret(self):
#         """Generates an 8-digit numeric code for email confirmation."""
#         self.email_confirmation_secret = '{:08d}'.format(random.randint(0, 99999999))
#         self.save()
    
#     def generate_mfa_secret_secret(self):
#         """Generates mfa secret"""
#         self.mfa_secret = pyotp.random_base32()
#         self.save()


#     def validate_email_confirmed(self):
#         """Marks the email as confirmed."""
#         self.email_confirmed = True
#         self.save()
    
#     def validate_mfa_enabled(self):
#         """Marks the mfa as enabled."""
#         self.mfa_enabled = True
#         self.save()

#     def disable_mfa_enabled(self):
#         """Marks the mfa as disabled."""
#         self.mfa_enabled = False
#         self.save()
    
#     def create_stripe_customer(self):
#         """Create the customer in Stripe and store the ID."""
#         stripe_customer = stripe.Customer.create(email=self.email)
#         self.stripe_customer_id = stripe_customer["id"]
#         self.save()
#         return stripe_customer

#     def update_stripe_customer(self):
#         """Update the Stripe customer with the latest account details."""
#         if self.stripe_customer_id:
#             try:
#                 stripe.Customer.modify(
#                     self.stripe_customer_id,
#                     email=self.email,
#                     name=self.name,
#                 )
#                 print(f"Updated Stripe customer: {self.stripe_customer_id}")
#             except Exception as e:
#                 print(f"Error updating Stripe customer: {e}")


#     def delete_stripe_customer(self):
#         """Delete the Stripe customer associated with this account."""
#         if self.stripe_customer_id:
#             try:
#                 stripe.Customer.delete(self.stripe_customer_id)
#                 self.stripe_customer_id = None
#                 self.save()
#                 print(f"Deleted Stripe customer: {self.stripe_customer_id}")
#             except Exception as e:
#                 print(f"Error deleting Stripe customer: {e}")

    
#     def save(self, *args, **kwargs):
#         CustomEmailValidator().validate(self.email)
#         # Check if this is a new user and Stripe ID is not set
#         if not self.stripe_customer_id and not self._state.adding:
#             stripe_customer = stripe.Customer.create(email=self.email)
#             self.stripe_customer_id = stripe_customer["id"]
#         # Hash the password if it's not already hashed
#         if self.password and not self.password.startswith('pbkdf2_'):
#             CustomPasswordValidator().validate(self.password)
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)
    
#     def delete(self, *args, **kwargs):
#         """Handle soft delete and remove Stripe customer."""
#         self.deleted = now()
#         self.save()
#         if self.stripe_customer_id:
#             self.delete_stripe_customer()


#     def __str__(self):
#         return self.username or self.email