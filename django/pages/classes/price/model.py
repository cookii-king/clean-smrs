import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
from ...models import Product

class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(max_length=3)
    recurring = models.JSONField(max_length=1024, null=True)
    product = models.ForeignKey(Product, to_field='stripe_product_id', on_delete=models.CASCADE, related_name='prices')
    unit_amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    stripe_price_id = models.CharField(max_length=255, blank=True, unique=True, null=True)  # Stripe product ID
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def create_stripe_price(self):
        """Creates a Stripe price and stores the price ID."""
        try:
            # Convert unit_amount from dollars to cents
            if isinstance(self.unit_amount, str):
                self.unit_amount = float(self.unit_amount)  # Ensure the input is a float

            unit_amount_cents = int(self.unit_amount * 100)  # Convert dollars to cents

            # Validate the unit_amount_cents
            if not (1 <= unit_amount_cents <= 100000000):  # Stripe max unit amount is $1,000,000 (in cents)
                raise ValueError(f"Invalid unit_amount: {self.unit_amount}. Must be between $0.01 and $1,000,000.00.")

            # Create a new Stripe price
            price = stripe.Price.create(
                unit_amount=unit_amount_cents,  # Stripe expects the amount in cents
                currency=self.currency,
                recurring=self.recurring if self.recurring else None,
                product=self.product.stripe_product_id,
            )
            # Store the Stripe price ID in the model
            self.stripe_price_id = price.id
            self.save()
            return price
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            raise Exception(f"Failed to create Stripe price: {e}")
        except Exception as e:
            print(f"Error: {e}")
            raise Exception(f"Failed to create Stripe price: {e}")



    def update_stripe_price(self, **kwargs):
        """Updates the Stripe price with the provided details."""
        try:
            # Update the Stripe price
            price = stripe.Price.modify(
                self.stripe_price_id,
                **kwargs
            )
            # Optionally update local fields if needed
            if 'unit_amount' in kwargs:
                self.unit_amount = kwargs['unit_amount'] / 100  # Convert back from cents
            if 'currency' in kwargs:
                self.currency = kwargs['currency']
            self.save()
            return price
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")
            raise Exception(f"Failed to update Stripe price: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            raise Exception(f"Failed to update Stripe price: {e}")

    def delete_stripe_price(self):
        """Deletes the Stripe price associated with this price."""
        try:
            # Archive the Stripe price (Stripe does not allow full deletion of prices)
            stripe.Price.modify(
                self.stripe_price_id,
                active=False
            )
            # Optionally, mark the local price as deleted
            self.deleted = now()
            self.save()
            print("Stripe price archived successfully.")
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(f"Stripe error: {e}")
            raise Exception(f"Failed to delete Stripe price: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            raise Exception(f"Failed to delete Stripe price: {e}")

    def __str__(self):
        return str(self.id)

    # Meta Class
    class Meta:
        db_table = "pages_price"