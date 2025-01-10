import uuid, pyotp, random
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from ...config.config import stripe
from system.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

from ...models import Account, Price, Plan

class Checkout(models.Model):
    CHECKOUT_MODE_CHOICES = [
        ('payment', 'Payment'),
        ('setup', 'Setup'),
        ('subscription', 'Subscription')
    ]
    CHECKOUT_PAYMENT_STATUS_CHOICES = [
        ('no_payment_required', 'No Payment Required'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid')
    ]
    CHECKOUT_STATUS_CHOICES = [
        ('complete', 'Complete'),
        ('expired', 'Expired'),
        ('open', 'Open')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Account, to_field='stripe_customer_id', on_delete=models.CASCADE,related_name='checkouts', null=True)
    mode = models.CharField(max_length=255, choices=CHECKOUT_MODE_CHOICES, default='payment')
    payment_status = models.CharField(max_length=255, choices=CHECKOUT_PAYMENT_STATUS_CHOICES, default='unpaid')
    status = models.CharField(max_length=255, choices=CHECKOUT_STATUS_CHOICES, null=True)
    stripe_checkout_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    success_url = models.CharField(max_length=255)
    return_url = models.CharField(max_length=255)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def add_item(self, price_id=None, plan_id=None, quantity=1):
        """
        Add a CheckoutLineItem to the checkout or update its quantity if it already exists.
        Either price_id or plan_id must be provided.
        """
        from ...models import Price, Plan  # Avoid circular imports

        if not price_id and not plan_id:
            raise ValueError("Either 'price_id' or 'plan_id' must be provided.")

        # Retrieve the price or plan
        if price_id:
            price = Price.objects.get(stripe_price_id=price_id)
        else:
            price = None

        if plan_id:
            plan = Plan.objects.get(stripe_plan_id=plan_id)
        else:
            plan = None

        # Check if the item already exists based on provided parameters
        checkout_item, created = self.checkout_line_items.get_or_create(
            price=price,  # Use the non-None value
            plan=plan,
            defaults={'quantity': quantity}
        )

        if not created:
            # Update the quantity if the item already exists
            checkout_item.quantity += quantity
            checkout_item.save()

        return checkout_item


    def update_item_quantity(self, price_id, quantity):
        """
        Update the quantity of a specific CheckoutLineItem in the checkout.
        """
        checkout_item = self.checkout_line_items.filter(price__stripe_price_id=price_id).first()
        if not checkout_item:
            raise ValueError("checkout item does not exist.")

        if quantity > 0:
            checkout_item.quantity = quantity
            checkout_item.save()
        else:
            checkout_item.delete()

        return checkout_item

    def remove_item(self, price_id):
        """
        Remove a CheckoutLineItem from the checkout.
        """
        checkout_item = self.checkout_line_items.filter(price__stripe_price_id=price_id).first()
        if checkout_item:
            checkout_item.delete()
        else:
            raise ValueError("checkout item does not exist.")

    def clear_items(self):
        """
        Remove all CheckoutLineItems from the checkout.
        """
        self.checkout_line_items.all().delete()

    def get_items(self):
        """
        Retrieve all CheckoutLineItems for this checkout.
        """
        return self.checkout_line_items.all()


    def create_stripe_session(self):
        """
        Create a Stripe Checkout Session for this checkout instance.
        """
        try:
            # Collect line items for the checkout session
            line_items = []
            for item in self.checkout_line_items.all():
                if item.price:  # If a price is associated
                    line_items.append({
                        "price": item.price.stripe_price_id,
                        "quantity": item.quantity,
                    })
                elif item.plan:  # If a plan is associated
                    line_items.append({
                        "price": item.plan.stripe_plan_id,
                        "quantity": item.quantity,
                    })
            print(f"line_items: ${line_items}")

            # Create the Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode=self.mode,  # Mode can be 'payment', 'setup', or 'subscription'
                line_items=line_items,
                success_url=self.success_url,
                cancel_url=self.return_url,
                customer=self.customer.stripe_customer_id if self.customer else None,
                currency="usd",  # Ensure Euro handling
            )

            # Save the session ID and update status
            self.stripe_checkout_id = session.id
            self.status = "open"
            self.save()

            return session.url  # Return the Stripe Checkout session URL

        except Exception as e:
            raise Exception(f"Error creating Stripe Checkout Session: {e}")
        

    def __str__(self):
        return str(self.id)

    # Meta Class
    class Meta:
        db_table = "pages_checkout"

class CheckoutLineItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    checkout = models.ForeignKey(Checkout, related_name='checkout_line_items', on_delete=models.CASCADE)
    price = models.ForeignKey(
        Price, 
        to_field='stripe_price_id', 
        on_delete=models.CASCADE, 
        related_name='checkout_line_items',
        null=True
    )
    plan = models.ForeignKey(
        Plan, 
        to_field='stripe_plan_id', 
        on_delete=models.CASCADE, 
        related_name='checkout_line_items',
        null=True
    )
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)


    def update_quantity(self, quantity):
        """
        Update the quantity of this checkout item.
        """
        if quantity > 0:
            self.quantity = quantity
            self.save()
        else:
            self.delete()

    def remove(self):
        """
        Remove this checkout item from the checkout.
        """
        self.delete()

    # Meta Class
    class Meta:
        db_table = "pages_checkout_line_item"