import uuid, secrets
from django.utils.timezone import now, timedelta
from django.db import models
from ...config.config import stripe
from ...models import Account, Price, Plan
from django.utils.timezone import is_aware, make_aware
class Subscription(models.Model):
    SUBSCRIPTION_STATUS_CHOICES = [
        ('incomplete', 'incomplete'),
        ('incomplete_expired', 'incomplete_expired'),
        ('trialing', 'trialing'),
        ('active', 'active'),
        ('past_due', 'past_due'),
        ('canceled', 'canceled'),
        ('unpaid', 'unpaid'),
        ('paused', 'paused'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Account, to_field='stripe_customer_id', 
        on_delete=models.CASCADE, 
        related_name='subscriptions'
    )
    status = models.CharField(max_length=255, choices=SUBSCRIPTION_STATUS_CHOICES, default=None)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def add_item(self, price_id=None, plan_id=None, quantity=1):
        """
        Add a SubscriptionItem to the subscription or update its quantity if it already exists.
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
        subscription_item, created = self.subscription_items.get_or_create(
            price=price,  # Use the non-None value
            plan=plan,
            defaults={'quantity': quantity}
        )

        if not created:
            # Update the quantity if the item already exists
            subscription_item.quantity += quantity
            subscription_item.save()

        return subscription_item
    
    def update_item_quantity(self, price_id, quantity):
        """
        Update the quantity of a specific SubscriptionItem in the subscription.
        """
        subscription_item = self.subscription_items.filter(price__stripe_price_id=price_id).first()
        if not subscription_item:
            raise ValueError("subscription item does not exist.")

        if quantity > 0:
            subscription_item.quantity = quantity
            subscription_item.save()
        else:
            subscription_item.delete()

        return subscription_item
    
    def remove_item(self, price_id):
        """
        Remove a SubscriptionItem from the subscription.
        """
        subscription_item = self.subscription_items.filter(price__stripe_price_id=price_id).first()
        if subscription_item:
            subscription_item.delete()
        else:
            raise ValueError("subscription item does not exist.")
    
    def clear_items(self):
        """
        Remove all SubscriptionItems from the subscription.
        """
        self.subscription_items.all().delete()

    def get_items(self):
        """
        Retrieve all SubscriptionItems for this subscription.
        """
        return self.subscription_items.all()


    def subscription_duration(self):
        """
        Calculate the duration of the subscription in days.
        """
        if self.deleted:
            end_date = self.deleted
        else:
            end_date = now()

        # Ensure both dates are aware or naive
        if is_aware(self.created) and not is_aware(end_date):
            end_date = make_aware(end_date)
        elif not is_aware(self.created) and is_aware(end_date):
            end_date = end_date.replace(tzinfo=None)

        return (end_date - self.created).days


    def cancel_subscription(self):
        """
        Cancel the Stripe subscription associated with this instance.
        """
        if not self.stripe_subscription_id:
            raise ValueError("This subscription does not have a Stripe subscription ID.")

        try:
            # Cancel the subscription in Stripe
            stripe.Subscription.delete(self.stripe_subscription_id)
            self.status = 'canceled'
            self.deleted = now()  # Record the cancellation time
            self.save()
            print(f"Subscription {self.stripe_subscription_id} has been canceled.")
        except Exception as e:
            print(f"Error canceling subscription {self.stripe_subscription_id}: {e}")
            raise


    def __str__(self):
        return str(self.id)

    # Meta Class
    class Meta:
        db_table = "pages_subscription"


class SubscriptionItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(
        Subscription, 
        on_delete=models.CASCADE, 
        related_name='subscription_items'
    )
    price = models.ForeignKey(
        Price, 
        to_field='stripe_price_id', 
        on_delete=models.CASCADE, 
        related_name='subscription_items',
        null=True
    )
    plan = models.ForeignKey(
        Plan, 
        to_field='stripe_plan_id', 
        on_delete=models.CASCADE, 
        related_name='subscription_items',
        null=True
    )
    quantity = models.PositiveIntegerField(default=1)
    stripe_subscription_item_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)


    def update_quantity(self, quantity):
        """
        Update the quantity of this subscription item.
        """
        if quantity > 0:
            self.quantity = quantity
            self.save()
        else:
            self.delete()
    
    def remove(self):
        """
        Remove this subscription item from the subscription.
        """
        self.delete()

    def __str__(self):
        return str(self.id)

    # Meta Class
    class Meta:
        db_table = "pages_subscription_item"