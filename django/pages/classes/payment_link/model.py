import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
from ...models import Price, Plan

class PaymentLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stripe_payment_link_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    def add_item(self, price_id=None, plan_id=None, quantity=1):
        """
        Add a PaymentLinkLineItem to the payment_link or update its quantity if it already exists.
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
        payment_link_item, created = self.payment_link_line_items.get_or_create(
            price= price,  # Use the non-None value
            plan=plan,
            defaults={'quantity': quantity}
        )

        if not created:
            # Update the quantity if the item already exists
            payment_link_item.quantity += quantity
            payment_link_item.save()

        return payment_link_item


    def update_item_quantity(self, price_id, quantity):
        """
        Update the quantity of a specific PaymentLinkLineItem in the payment_link.
        """
        payment_link_item = self.payment_link_line_items.filter(price__stripe_price_id=price_id).first()
        if not payment_link_item:
            raise ValueError("payment_link item does not exist.")

        if quantity > 0:
            payment_link_item.quantity = quantity
            payment_link_item.save()
        else:
            payment_link_item.delete()

        return payment_link_item

    def remove_item(self, price_id):
        """
        Remove a PaymentLinkLineItem from the payment_link.
        """
        payment_link_item = self.payment_link_line_items.filter(price__stripe_price_id=price_id).first()
        if payment_link_item:
            payment_link_item.delete()
        else:
            raise ValueError("payment_link item does not exist.")

    def clear_items(self):
        """
        Remove all PaymentLinkLineItems from the payment_link.
        """
        self.payment_link_line_items.all().delete()

    def get_items(self):
        """
        Retrieve all PaymentLinkLineItems for this payment_link.
        """
        return self.payment_link_line_items.all()

    # def create_or_update_stripe_payment_link(self):
    #     """
    #     Create or update a Stripe payment_link based on the current items.
    #     """
    #     items = [
    #         {
    #             "price": item.plan.stripe_plan_id or item.plan.stripe_plan_id,
    #             "quantity": item.quantity
    #         } for item in self.get_items()
    #     ]

    #     print(f"model items: ${self.payment_link_line_items.all()}")

    #     if not items:
    #         raise ValueError("No items to create or update payment_link.")

    #     if self.stripe_payment_link_id:
    #         # Update existing Stripe payment_link
    #         stripe.PaymentLink.modify(self.stripe_payment_link_id, line_items=items)
    #     else:
    #         # Create a new Stripe payment_link
    #         stripe_payment_link = stripe.PaymentLink.create(
    #             # customer=self.customer.stripe_customer_id,
    #             line_items=items
    #         )
    #         self.stripe_payment_link_id = stripe_payment_link['id']
    #         self.save()

    def create_or_update_stripe_payment_link(self):
        """
        Create or update a Stripe payment_link based on the current items.
        """
        items = []

        # Iterate through all payment link items and add to the items list
        for item in self.get_items():
            if item.price:
                stripe_id = item.price.stripe_price_id
            elif item.plan:
                stripe_id = item.plan.stripe_plan_id
            else:
                raise ValueError("PaymentLinkLineItem must have either a price or a plan.")

            items.append({
                "price": stripe_id,
                "quantity": item.quantity
            })

        print(f"model items: {items}")

        if not items:
            raise ValueError("No items to create or update payment link.")

        if self.stripe_payment_link_id:
            # Update existing Stripe payment link
            stripe.PaymentLink.modify(self.stripe_payment_link_id, line_items=items)
        else:
            # Create a new Stripe payment link
            stripe_payment_link = stripe.PaymentLink.create(
                line_items=items
            )
            self.stripe_payment_link_id = stripe_payment_link['id']
            self.save()


    def __str__(self):
        return str(self.id)

class PaymentLinkLineItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_link = models.ForeignKey(PaymentLink, related_name='payment_link_line_items', on_delete=models.CASCADE)
    price = models.ForeignKey(
        Price, 
        to_field='stripe_price_id', 
        on_delete=models.CASCADE, 
        related_name='payment_link_line_items',
        null=True
    )
    plan = models.ForeignKey(
        Plan, 
        to_field='stripe_plan_id', 
        on_delete=models.CASCADE, 
        related_name='payment_link_line_items',
        null=True
    )
    quantity = models.PositiveIntegerField(default=1)

    def update_quantity(self, quantity):
        """
        Update the quantity of this payment_link item.
        """
        if quantity > 0:
            self.quantity = quantity
            self.save()
        else:
            self.delete()

    def remove(self):
        """
        Remove this payment_link item from the payment_link.
        """
        self.delete()

    def __str__(self):
        return str(self.id)

