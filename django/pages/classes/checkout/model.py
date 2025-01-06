import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
from ...models import Price, Plan, Account

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
    customer = models.ForeignKey(Account, to_field='stripe_customer_id', on_delete=models.CASCADE)
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

    def create_or_update_stripe_checkout(self):
        """
        Create or update a Stripe checkout based on the current items.
        """
        items = []

        # Iterate through all checkout items and add to the items list
        for item in self.get_items():
            if item.price:
                stripe_id = item.price.stripe_price_id
            elif item.plan:
                stripe_id = item.plan.stripe_plan_id
            else:
                raise ValueError("CheckoutLineItem must have either a price or a plan.")

            items.append({
                "price": stripe_id,
                "quantity": item.quantity
            })

        print(f"model items: {items}")

        if not items:
            raise ValueError("No items to create or update checkout.")

        # Generate the success and cancel URLs using the checkout object's ID
        success_url = f"{self.success_url}?checkout={self.id}"
        cancel_url = f"{self.return_url}?checkout={self.id}"

        if self.stripe_checkout_id:
            # Update existing Stripe checkout
            stripe.checkout.Session.modify(
                self.stripe_checkout_id,
                success_url=success_url,
                cancel_url=cancel_url
            )
        else:
            # Create a new Stripe checkout
            stripe_checkout = stripe.checkout.Session.create(
                success_url=success_url,
                cancel_url=cancel_url,
                line_items=items,
                mode=self.mode,
                customer=self.customer.stripe_customer_id
            )
            self.stripe_checkout_id = stripe_checkout['id']
            self.save()



    # def create_or_update_stripe_checkout(self):
    #     """
    #     Create or update a Stripe checkout based on the current items.
    #     """
    #     items = []

    #     # Iterate through all checkout items and add to the items list
    #     for item in self.get_items():
    #         if item.price:
    #             stripe_id = item.price.stripe_price_id
    #         elif item.plan:
    #             stripe_id = item.plan.stripe_plan_id
    #         else:
    #             raise ValueError("CheckoutLineItem must have either a price or a plan.")

    #         items.append({
    #             "price": stripe_id,
    #             "quantity": item.quantity
    #         })

    #     print(f"model items: {items}")

    #     if not items:
    #         raise ValueError("No items to create or update checkout.")

    #     if self.stripe_checkout_id:
    #         # Update existing Stripe checkout
    #         stripe.checkout.Session.modify(self.stripe_checkout_id)
    #     else:
    #         # Create a new Stripe checkout
    #         stripe_checkout = stripe.checkout.Session.create(
    #             success_url=f"${self.success_url}?session_id=${self.stripe_checkout_id}",
    #             cancel_url=f"${self.return_url}?session_id=${self.stripe_checkout_id}",
    #             line_items=items,
    #             mode=self.mode,
    #             customer=self.customer.stripe_customer_id
    #         )
    #         self.stripe_checkout_id = stripe_checkout['id']
    #         self.save()


    def __str__(self):
        return str(self.id)

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

    def __str__(self):
        return str(self.id)
