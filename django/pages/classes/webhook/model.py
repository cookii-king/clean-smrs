import uuid
from django.db import models
from django.utils.timezone import now
from ...config.config import stripe
from ...models import Product, Account, Cart, ApiKey,    Checkout,CheckoutLineItem, Order, OrderItem,  PaymentLink, Plan, Price, Subscription
from django.core.mail import send_mail

class Webhook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=255)
    data = models.JSONField()  # Store the raw payload for reference
    processed = models.BooleanField(default=False)
    created = models.DateTimeField(default=now) 

    def process_event(self): 
        try:
            if self.event_type in ['product.created', 'product.updated']:
                self.process_product()
            elif self.event_type in ['customer.created', 'customer.updated', 'customer.deleted']:
                self.process_customer()
                #   self.process_customer_deleted()
            elif self.event_type in ['checkout.session.async_payment_failed', 'checkout.session.async_payment_succeeded', 'checkout.session.completed', 'checkout.session.expired']:
              self.process_checkout()
            elif self.event_type in ['payment_link.created', 'payment_link.updated']:
              self.process_payment_link()
            elif self.event_type in ['plan.created', 'plan.updated', 'plan.deleted']:
              self.process_plan()
            elif self.event_type in ['price.created', 'price.updated', 'price.deleted']:
              self.process_price()
            elif self.event_type in ['customer.subscription.created', 'customer.subscription.paused', 'customer.subscription.deleted', 'customer.subscription.pending_update_applied', 'customer.subscription.pending_update_expired', 'customer.subscription.resumed', 'customer.subscription.trial_will_end', 'customer.subscription.updated']:
              self.process_subscription()
            else:
                print(f"Unhandled event type: {self.event_type}")
            self.processed = True
            self.save()
        except Exception as e:
            print(f"Error processing event {self.event_id}: {str(e)}")


    def process_customer(self):
        """
        Process 'customer.created' or 'customer.updated' events from Stripe.
        """
        data = self.data.get('object', {})
        if not data:
            raise ValueError("No customer data in event payload.")

        stripe_customer_id = data.get('id')
        name = data.get('name') or "Unnamed Customer"
        email = data.get('email')
        description = data.get('description', '')

        if not email:
            raise ValueError("Email is required for customer creation.")
        
        customer = Account.objects.filter(stripe_customer_id=stripe_customer_id).first()

        print(f"process customer: ${customer}")
        if customer is not None:
            # Update the existing customer
            print(f"Account already exists with Stripe ID: {stripe_customer_id}")
            customer.name = name
            customer.email = email
            customer.description = description
            customer.save()
        else:
            # Create a new customer
            print(f"Creating new customer with Stripe ID: {stripe_customer_id}")
            new_customer = Account(
                stripe_customer_id=stripe_customer_id,
                username=email,  # Use email as the default username
                name=name,
                email=email,
                description=description,
            )
            print(f"Account Object: {new_customer.stripe_customer_id}")
            new_customer.save()  # Ensure save completes before further processing

        # Use get_or_create to handle object creation or retrieval
        customer, created = Account.objects.get_or_create(
            stripe_customer_id=stripe_customer_id,
            defaults={
                'username': email,  # Use email as the default username
                'name': name,
                'email': email,
                'description': description,
            }
        )

        if not created:
            # Update existing customer if not newly created
            customer.name = name
            customer.email = email
            customer.description = description
            customer.save()

        print(f"Customer {'created' if created else 'updated'} with Stripe ID: {stripe_customer_id}")

    def process_product(self):
        """
        Process 'product.created' or 'product.updated' events from Stripe.
        """
        data = self.data.get('object', {})
        if not data:
            raise ValueError("No product data in event payload.")

        stripe_product_id = data.get('id')
        name = data.get('name')
        description = data.get('description', '')

        # Check if the product exists
        product = Product.objects.filter(stripe_product_id=stripe_product_id).first()
        if product:
            # Update the existing product
            print(f"Product already exists with Stripe ID: {stripe_product_id}")
            product.name = name
            product.description = description
            product.save()  # This will automatically call update_stripe_product
        else:
            # Create a new product
            print(f"Creating new product with Stripe ID: {stripe_product_id}")
            Product.objects.create(
                stripe_product_id=stripe_product_id,
                name=name,
                description=description
            )

    # def process_checkout(self):
    #     """
    #     Process 'checkout.session.async_payment_failed', 'checkout.session.async_payment_succeeded', 
    #     'checkout.session.completed', or 'checkout.session.expired' events from Stripe.
    #     """
    #     event_type = self.event_type
    #     print(f"checkout event type: {event_type}")
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No checkout data in event payload.")

    #     stripe_checkout_id = data.get('id')
    #     customer_id = data.get('customer')
    #     mode = data.get('mode')
    #     payment_status = data.get('payment_status')
    #     status = data.get('status')

    #     # Retrieve the associated Account using the Stripe customer ID
    #     customer = Account.objects.filter(stripe_customer_id=customer_id).first()
    #     if not customer:
    #         raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")

    #     # Fetch line items from Stripe API
    #     line_items = stripe.checkout.Session.list_line_items(stripe_checkout_id)

    #     # Check if the checkout exists
    #     checkout, created = Checkout.objects.get_or_create(
    #         stripe_checkout_id=stripe_checkout_id,
    #         success_url = f"/checkout/success/?session_id={stripe_checkout_id}",
    #         defaults={
    #             'customer': customer,
    #             'mode': mode,
    #             'payment_status': payment_status,
    #             'status': status,
    #         }
    #     )

    #     if not created:
    #         # Update the existing checkout
    #         print(f"Updating checkout with Stripe ID: {stripe_checkout_id}")
    #         checkout.customer = customer
    #         checkout.mode = mode
    #         checkout.payment_status = payment_status
    #         checkout.status = status
    #         checkout.save()

    #     # Update the success_url to include the session_id
    #     success_url = f"/checkout/success/?session_id={stripe_checkout_id}"
    #     if checkout.success_url != success_url:
    #         checkout.success_url = success_url
    #         checkout.save()

    #     # Save line items and create an order
    #     order = Order.objects.create(
    #         customer=customer,
    #         checkout=checkout
    #     )

    #     for item in line_items['data']:
    #         price_id = item['price']['id']
    #         quantity = item['quantity']

    #         # Ensure price exists in your database
    #         price = Price.objects.filter(stripe_price_id=price_id).first()
    #         if not price:
    #             print(f"Price {price_id} not found in the database. Skipping.")
    #             continue

    #         # Create order item
    #         OrderItem.objects.create(
    #             order=order,
    #             product=price.product,  # Assuming a Price is linked to a Product
    #             price=price,
    #             quantity=quantity
    #         )

    #     print(f"Order created with ID: {order.id} for checkout session {stripe_checkout_id}")


 

    def process_checkout(self):
        """
        Process 'checkout.session.async_payment_failed', 'checkout.session.async_payment_succeeded', 
        'checkout.session.completed', or 'checkout.session.expired' events from Stripe.
        """
        event_type = self.event_type
        print(f"checkout event type: {event_type}")
        data = self.data.get('object', {})
        if not data:
            raise ValueError("No checkout data in event payload.")

        stripe_checkout_id = data.get('id')
        customer_id = data.get('customer')
        mode = data.get('mode')
        payment_status = data.get('payment_status')
        status = data.get('status')

        # Retrieve the associated Account using the Stripe customer ID
        customer = Account.objects.filter(stripe_customer_id=customer_id).first()
        if not customer:
            raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")

        # Fetch line items from Stripe API
        line_items = stripe.checkout.Session.list_line_items(stripe_checkout_id)

        # Check if the checkout exists
        checkout, created = Checkout.objects.get_or_create(
            stripe_checkout_id=stripe_checkout_id,
            defaults={
                'customer': customer,
                'mode': mode,
                'payment_status': payment_status,
                'status': status,
            }
        )

        if not created:
            # Update the existing checkout
            print(f"Updating checkout with Stripe ID: {stripe_checkout_id}")
            checkout.customer = customer
            checkout.mode = mode
            checkout.payment_status = payment_status
            checkout.status = status
            checkout.save()

        # Save line items and create an order
        order = Order.objects.create(
            customer=customer,
            checkout=checkout
        )

        order_items = []
        for item in line_items['data']:
            price_id = item['price']['id']
            quantity = item['quantity']

            # Ensure price exists in your database
            price = Price.objects.filter(stripe_price_id=price_id).first()
            if not price:
                print(f"Price {price_id} not found in the database. Skipping.")
                continue

            # Create order item
            order_item = OrderItem.objects.create(
                order=order,
                product=price.product,  # Assuming a Price is linked to a Product
                price=price,
                quantity=quantity
            )
            order_items.append(order_item)

        print(f"Order created with ID: {order.id} for checkout session {stripe_checkout_id}")

        # Send an email to the customer
        self.send_order_email(customer, order, order_items)

    def send_order_email(self, customer, order, order_items):
        """Send an email to the customer with their order details."""
        subject = "Your Order Details"
        message = (
            f"Hello {customer.name},\n\n"
            "Thank you for your purchase! Here are the details of your order:\n\n"
            f"Order ID: {order.id}\n"
            f"Checkout ID: {order.checkout.id}\n"
            f"Date: {order.created.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "Items:\n"
        )

        total_amount = 0
        for item in order_items:
            # Convert price from cents to dollars
            price_in_dollars = item.price.unit_amount / 100
            total_item_price = price_in_dollars * item.quantity
            total_amount += total_item_price

            message += (
                f"- {item.product.name} (Quantity: {item.quantity}) - "
                f"${price_in_dollars:.2f} each\n"
            )

        message += f"\nTotal Amount: ${total_amount:.2f}\n\n"
        message += "We hope you enjoy your purchase!\n\nBest regards,\nThe Team"

        from_email = "no-reply@example.com"  # Replace with your sender email
        recipient_list = [customer.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            print(f"Order email sent to {customer.email}")
        except Exception as e:
            print(f"Error sending order email: {e}")
            raise



    # def process_checkout(self):
    #     """
    #     Process 'checkout.session.async_payment_failed', 'checkout.session.async_payment_succeeded', 
    #     'checkout.session.completed', or 'checkout.session.expired' events from Stripe.
    #     """
    #     event_type = self.event_type
    #     print(f"checkout event type: {event_type}")
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No checkout data in event payload.")

    #     stripe_checkout_id = data.get('id')
    #     customer_id = data.get('customer')
    #     mode = data.get('mode')
    #     payment_status = data.get('payment_status')
    #     status = data.get('status')

    #     # Retrieve the associated Account using the Stripe customer ID
    #     customer = Account.objects.filter(stripe_customer_id=customer_id).first()
    #     if not customer:
    #         raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")

    #     # Fetch line items from Stripe API
    #     line_items = stripe.checkout.Session.list_line_items(stripe_checkout_id)

    #     # Check if the checkout exists
    #     checkout = Checkout.objects.filter(stripe_checkout_id=stripe_checkout_id).first()
    #     if checkout:
    #         # Update the existing checkout
    #         print(f"Checkout already exists with Stripe ID: {stripe_checkout_id}")
    #         checkout.customer = customer
    #         checkout.mode = mode
    #         checkout.payment_status = payment_status
    #         checkout.status = status
    #         checkout.save()  # Automatically call update_stripe_checkout

    #         # Save line items
    #         for item in line_items['data']:
    #             price_id = item['price']['id']
    #             quantity = item['quantity']

    #             # Ensure price exists in your database
    #             price = Price.objects.filter(stripe_price_id=price_id).first()
    #             if not price:
    #                 print(f"Price {price_id} not found in the database. Skipping.")
    #                 continue

    #             # Save checkout line item
    #             CheckoutLineItem.objects.get_or_create(
    #                 checkout=checkout,
    #                 price=price,
    #                 defaults={'quantity': quantity}
    #             )
    #     else:
    #         # Create a new checkout
    #         print(f"Creating new checkout with Stripe ID: {stripe_checkout_id}")
    #         checkout = Checkout.objects.create(
    #             stripe_checkout_id=stripe_checkout_id,
    #             customer=customer,
    #             mode=mode,
    #             payment_status=payment_status,
    #             status=status
    #         )

    #         # Save line items
    #         for item in line_items['data']:
    #             price_id = item['price']['id']
    #             quantity = item['quantity']

    #             # Ensure price exists in your database
    #             price = Price.objects.filter(stripe_price_id=price_id).first()
    #             if not price:
    #                 print(f"Price {price_id} not found in the database. Skipping.")
    #                 continue

    #             # Save checkout line item
    #             CheckoutLineItem.objects.create(
    #                 checkout=checkout,
    #                 price=price,
    #                 quantity=quantity
    #             )


    # def process_checkout(self):
    #     """
    #     Process 'checkout.session.async_payment_failed', 'checkout.session.async_payment_succeeded', 'checkout.session.completed' or 'checkout.session.expired' events from Stripe.
    #     """
    #     event_type = self.event_type
    #     print(f"checkout event type: ${event_type}")
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No checkout data in event payload.")

    #     stripe_checkout_id = data.get('id')
    #     customer_id = data.get('customer')
    #     mode = data.get('mode')
    #     payment_status = data.get('payment_status')
    #     status = data.get('status')

    #     # Retrieve the associated Account using the Stripe customer ID
    #     customer = Account.objects.filter(stripe_customer_id=customer_id).first()
    #     if not customer:
    #         raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")

    #     # Check if the checkout exists
    #     checkout = Checkout.objects.filter(stripe_checkout_id=stripe_checkout_id).first()
    #     if checkout:
    #         # Update the existing checkout
    #         print(f"Checkout already exists with Stripe ID: {stripe_checkout_id}")
    #         checkout.customer = customer
    #         checkout.mode = mode
    #         checkout.payment_status = payment_status
    #         checkout.status=status
    #         checkout.save()  # This will automatically call update_stripe_checkout
    #         if checkout.status in ['complete'] and checkout.payment_status in ['paid']:
    #             # # Retrieve the associated ApiKey using the Account
    #             # api_key = ApiKey.objects.filter(account=customer).first()
    #             # if not api_key:
    #             #     raise ValueError(f"ApiKey with Account {customer.id} not found.")
    #             if checkout.mode in ['subscription']:
    #                 # pass
    #                 # Ensure the API key exists or generate a new one
    #                 api_key, created = ApiKey.objects.get_or_create(account=customer)
    #                 if created:
    #                     print(f"New API key created for account {customer.id}: {api_key.key}")
    #                     api_key.generate_key()
    #                 else:
    #                     print(f"Existing API key retrieved for account {customer.id}: {api_key.key}")
    #                 api_key.active = True
    #                 api_key.save()


    #     else:
    #         # Create a new checkout
    #         print(f"Creating new checkout with Stripe ID: {stripe_checkout_id}")
    #         Checkout.objects.create(
    #             stripe_checkout_id=stripe_checkout_id,
    #             customer=customer,
    #             mode=mode,
    #             payment_status=payment_status,
    #             status=status
    #         )

    def process_subscription(self):
        """
        Process 'customer.subscription.created', 'customer.subscription.paused', or 'customer.subscription.deleted' events from Stripe.
        """
        data = self.data.get('object', {})
        if not data:
            raise ValueError("No subscription data in event payload.")

        stripe_subscription_id = data.get('id')
        customer_id = data.get('customer')
        status = data.get('status')
        items_data = data.get('items', {}).get('data', [])

        # Retrieve the associated Account using the Stripe customer ID
        customer = Account.objects.filter(stripe_customer_id=customer_id).first()
        if not customer:
            raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")

        # Get or create the subscription
        subscription, created = Subscription.objects.get_or_create(
            stripe_subscription_id=stripe_subscription_id,
            customer=customer,
            defaults={'status': status}
        )

        if not created:
            subscription.status = status
            subscription.save()

        print(f"{'Created' if created else 'Updated'} subscription with Stripe ID: {stripe_subscription_id}")

        # Process subscription items
        for item_data in items_data:
            price_id = item_data.get('price', {}).get('id')  # New price ID from Stripe
            stripe_item_id = item_data.get('id')  # Stripe subscription item ID
            quantity = item_data.get('quantity', 1)

            if not price_id:
                print("Skipping item with missing price ID.")
                continue

            # Ensure the price exists in the database
            price = Price.objects.filter(stripe_price_id=price_id).first()
            if not price:
                print(f"Price with Stripe ID {price_id} not found. Skipping.")
                continue

            # Add or update the subscription item
            subscription_item, item_created = subscription.subscription_items.get_or_create(
                stripe_subscription_item_id=stripe_item_id,
                defaults={
                    'price': price,
                    'quantity': quantity,
                }
            )

            if not item_created:
                # Update the subscription item with new values
                subscription_item.price = price
                subscription_item.quantity = quantity
                subscription_item.save()

            print(f"{'Added' if item_created else 'Updated'} item with Price ID: {price_id}, Stripe Item ID: {stripe_item_id}, Quantity: {quantity}.")

        # Optional: Remove subscription items that are no longer in Stripe
        existing_stripe_item_ids = [item['id'] for item in items_data]
        subscription.subscription_items.exclude(stripe_subscription_item_id__in=existing_stripe_item_ids).delete()

        print(f"Processed subscription items for subscription ID: {stripe_subscription_id}")


    # def process_subscription(self):
    #     """
    #     Process 'customer.subscription.created', 'customer.subscription.paused', or 'customer.subscription.deleted' events from Stripe.
    #     """
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No subscription data in event payload.")

    #     stripe_subscription_id = data.get('id')
    #     customer_id = data.get('customer')
    #     status = data.get('status')
    #     items_data = data.get('items', {}).get('data', [])

    #     # Retrieve the associated Account using the Stripe customer ID
    #     customer = Account.objects.filter(stripe_customer_id=customer_id).first()
    #     if not customer:
    #         raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")

    #     # Get or create the subscription
    #     subscription, created = Subscription.objects.get_or_create(
    #         stripe_subscription_id=stripe_subscription_id,
    #         customer=customer,
    #         defaults={'status': status}
    #     )

    #     if not created:
    #         subscription.status = status
    #         subscription.save()

    #     print(f"{'Created' if created else 'Updated'} subscription with Stripe ID: {stripe_subscription_id}")

    #     # Process subscription items
    #     for item_data in items_data:
    #         price_id = item_data.get('price', {}).get('id')
    #         stripe_item_id = item_data.get('id')  # Stripe subscription item ID
    #         quantity = item_data.get('quantity', 1)

    #         if not price_id:
    #             print("Skipping item with missing price ID.")
    #             continue

    #         # Ensure the price exists in the database
    #         price = Price.objects.filter(stripe_price_id=price_id).first()
    #         if not price:
    #             print(f"Price with Stripe ID {price_id} not found. Skipping.")
    #             continue

    #         # Add or update the subscription item
    #         subscription_item, item_created = subscription.subscription_items.get_or_create(
    #             price=price,
    #             defaults={
    #                 'quantity': quantity,
    #                 'stripe_subscription_item_id': stripe_item_id
    #             }
    #         )

    #         if not item_created:
    #             subscription_item.quantity = quantity
    #             subscription_item.stripe_subscription_item_id = stripe_item_id  # Update the Stripe item ID
    #             subscription_item.save()

    #         print(f"{'Added' if item_created else 'Updated'} item with Price ID: {price_id}, Stripe Item ID: {stripe_item_id}, Quantity: {quantity}.")

    #     # Optional: Remove subscription items that are no longer in Stripe
    #     existing_price_ids = [item['price']['id'] for item in items_data]
    #     subscription.subscription_items.exclude(price__stripe_price_id__in=existing_price_ids).delete()

    #     print(f"Processed subscription items for subscription ID: {stripe_subscription_id}")


    # def process_subscription(self):
    #     """
    #     Process 'customer.subscription.created', 'customer.subscription.paused', or 'customer.subscription.deleted' events from Stripe.
    #     """
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No subscription data in event payload.")

    #     stripe_subscription_id = data.get('id')
    #     customer_id = data.get('customer')
    #     status = data.get('status')
    #     items_data = data.get('items', {}).get('data', [])

    #     # Retrieve the associated Account using the Stripe customer ID
    #     customer = Account.objects.filter(stripe_customer_id=customer_id).first()
    #     if not customer:
    #         raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")

    #     # Get or create the subscription
    #     subscription, created = Subscription.objects.get_or_create(
    #         stripe_subscription_id=stripe_subscription_id,
    #         customer=customer,
    #         defaults={'status': status}
    #     )

    #     if not created:
    #         subscription.status = status
    #         subscription.save()

    #     print(f"{'Created' if created else 'Updated'} subscription with Stripe ID: {stripe_subscription_id}")

    #     # Process subscription items
    #     for item_data in items_data:
    #         price_id = item_data.get('price', {}).get('id')
    #         quantity = item_data.get('quantity', 1)

    #         if not price_id:
    #             print("Skipping item with missing price ID.")
    #             continue

    #         # Ensure the price exists in the database
    #         price = Price.objects.filter(stripe_price_id=price_id).first()
    #         if not price:
    #             print(f"Price with Stripe ID {price_id} not found. Skipping.")
    #             continue

    #         # Add or update the subscription item
    #         subscription_item, item_created = subscription.subscription_items.get_or_create(
    #             price=price,
    #             defaults={'quantity': quantity}
    #         )

    #         if not item_created:
    #             subscription_item.quantity = quantity
    #             subscription_item.save()

    #         print(f"{'Added' if item_created else 'Updated'} item with Price ID: {price_id} (Quantity: {quantity}).")

    #     # Optional: Remove subscription items that are no longer in Stripe
    #     existing_price_ids = [item['price']['id'] for item in items_data]
    #     subscription.subscription_items.exclude(price__stripe_price_id__in=existing_price_ids).delete()

    #     print(f"Processed subscription items for subscription ID: {stripe_subscription_id}")


    # def process_subscription(self):
    #     """
    #     Process 'customer.subscription.created', 'customer.subscription.paused' or 'customer.subscription.deleted' events from Stripe.
    #     """
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No subscription data in event payload.")

    #     stripe_subscription_id = data.get('id')
    #     customer_id = data.get('customer')
    #     status = data.get('status')

    #     # Retrieve the associated Account using the Stripe customer ID
    #     customer = Account.objects.filter(stripe_customer_id=customer_id).first()
    #     if not customer:
    #         raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")

    #     # Check if the subscription exists
    #     subscription = Subscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()
    #     if subscription:
    #         # Update the existing subscription
    #         print(f"Subscription already exists with Stripe ID: {stripe_subscription_id}")
    #         subscription.customer = customer
    #         subscription.status=status
    #         subscription.save()  # This will automatically call update_stripe_subscription
    #         if subscription.status in ['active']:
    #             pass
    #             # # Retrieve the associated ApiKey using the Account
    #             # api_key = ApiKey.objects.filter(account=customer).first()
    #             # if not api_key:
    #             #     raise ValueError(f"ApiKey with Account {customer.id} not found.")
    #             # if subscription.mode in ['subscription']:
    #             #     # pass
    #             #     # Ensure the API key exists or generate a new one
    #             #     api_key, created = ApiKey.objects.get_or_create(account=customer)
    #             #     if created:
    #             #         print(f"New API key created for account {customer.id}: {api_key.key}")
    #             #         api_key.generate_key()
    #             #     else:
    #             #         print(f"Existing API key retrieved for account {customer.id}: {api_key.key}")
    #             #     api_key.active = True
    #             #     api_key.save()


    #     else:
    #         # Create a new subscription
    #         print(f"Creating new subscription with Stripe ID: {stripe_subscription_id}")
    #         Subscription.objects.create(
    #             stripe_subscription_id=stripe_subscription_id,
    #             customer=customer,
    #             status=status
    #         )

    def process_payment_link(self):
        """
        Process 'payment_link.created' or 'payment_link.updated' events from Stripe.
        """
        data = self.data.get('object', {})
        if not data:
            raise ValueError("No payment_link data in event payload.")

        stripe_payment_link_id = data.get('id')

        # Check if the payment_link exists
        payment_link = PaymentLink.objects.filter(stripe_payment_link_id=stripe_payment_link_id).first()
        if payment_link:
            # Update the existing payment_link
            print(f"PaymentLink already exists with Stripe ID: {stripe_payment_link_id}")
            # payment_link.name = name
            payment_link.save()  # This will automatically call update_stripe_payment_link
        else:
            # Create a new payment_link
            print(f"Creating new payment_link with Stripe ID: {stripe_payment_link_id}")
            PaymentLink.objects.create(
                stripe_payment_link_id=stripe_payment_link_id,

            )

   
    def process_plan(self):
        """
        Process 'plan.created', 'plan.updated' or 'plan.deleted' events from Stripe.
        """
        data = self.data.get('object', {})
        if not data:
            raise ValueError("No plan data in event payload.")

        stripe_plan_id = data.get('id')
        currency = data.get('currency')
        interval = data.get('interval')
        product_id = data.get('product')  # This is the Stripe product ID
        amount = data.get('amount') / 100  # Convert cents to dollars

        # Retrieve the associated Product using the Stripe product ID
        product = Product.objects.filter(stripe_product_id=product_id).first()
        if not product:
            raise ValueError(f"Product with Stripe product ID {product_id} not found.")

        # Check if the plan exists
        plan = Plan.objects.filter(stripe_plan_id=stripe_plan_id).first()
        if plan:
            # Update the existing plan
            print(f"Plan already exists with Stripe ID: {stripe_plan_id}")
            plan.currency = currency
            plan.interval = interval
            plan.product = product
            plan.amount = amount
            plan.save()
        else:
            # Create a new plan
            print(f"Creating new plan with Stripe ID: {stripe_plan_id}")
            Plan.objects.create(
                stripe_plan_id=stripe_plan_id,
                currency=currency,
                interval=interval,
                product=product,
                amount=amount,
            )


    # def process_plan(self):
    #     """
    #     Process 'plan.created', 'plan.updated' or 'plan.deleted' events from Stripe.
    #     """
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No plan data in event payload.")

    #     stripe_plan_id = data.get('id')
    #     currency = data.get('id')
    #     interval = data.get('interval')
    #     product = data.get('product')
    #     amount = data.get('amount')

    #     # Check if the plan exists
    #     plan = Plan.objects.filter(stripe_plan_id=stripe_plan_id).first()
    #     fetched_product = Product.objects.filter(stripe_product_id=product).first()
    #     if plan:
    #         # Update the existing plan
    #         print(f"Plan already exists with Stripe ID: {stripe_plan_id}")
    #         plan.currency = currency
    #         plan.interval = interval
    #         plan.product = product
    #         plan.amount = amount
    #         plan.save()  # This will automatically call update_stripe_plan
    #     else:
    #         # Create a new plan
    #         print(f"Creating new plan with Stripe ID: {stripe_plan_id}")
    #         Plan.objects.create(
    #             stripe_plan_id=stripe_plan_id,
    #             currency=currency,
    #             interval=interval,
    #             product=fetched_product,
    #             amount=amount,
    #         )

    def process_price(self):
        """
        Process 'price.created', 'price.updated' or 'price.deleted' events from Stripe.
        """
        data = self.data.get('object', {})
        if not data:
            raise ValueError("No price data in event payload.")

        stripe_price_id = data.get('id')
        currency = data.get('currency')
        recurring = data.get('recurring', None)
        product_id = data.get('product')  # This is the Stripe product ID
        unit_amount = data.get('unit_amount', 0) / 100  # Convert cents to dollars

        # Retrieve the associated Product using the Stripe product ID
        product = Product.objects.filter(stripe_product_id=product_id).first()
        if not product:
            raise ValueError(f"Product with Stripe product ID {product_id} not found.")

        # Check if the price exists
        price = Price.objects.filter(stripe_price_id=stripe_price_id).first()
        if price:
            # Update the existing price
            print(f"Price already exists with Stripe ID: {stripe_price_id}")
            price.currency = currency
            price.recurring = recurring
            price.product = product
            price.unit_amount = unit_amount
            price.save()
        else:
            # Create a new price
            print(f"Creating new price with Stripe ID: {stripe_price_id}")
            Price.objects.create(
                stripe_price_id=stripe_price_id,
                currency=currency,
                recurring=recurring,
                product=product,
                unit_amount=unit_amount,
            )

    
    # def process_price(self):
    #     """
    #     Process 'price.created', 'price.updated' or 'price.deleted' events from Stripe.
    #     """
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No price data in event payload.")

    #     stripe_price_id = data.get('id')
    #     currency = data.get('currency')
    #     recurring = data.get('recurring')
    #     product = data.get('product')
    #     unit_amount = data.get('unit_amount')

    #     # Check if the price exists
    #     price = Price.objects.filter(stripe_price_id=stripe_price_id).first()
    #     fetched_product = Product.objects.filter(stripe_product_id=product).first()
    #     if price:
    #         # Update the existing price
    #         print(f"Price already exists with Stripe ID: {stripe_price_id}")
    #         price.currency = currency
    #         price.recurring = recurring
    #         price.product = fetched_product
    #         price.unit_amount = unit_amount
    #         price.save()  # This will automatically call update_stripe_price
    #     else:
    #         # Create a new price
    #         print(f"Creating new price with Stripe ID: {stripe_price_id}")
    #         Price.objects.create(
    #             stripe_price_id=stripe_price_id,
    #             currency=currency,
    #             recurring=recurring,
    #             product=fetched_product,
    #             unit_amount=unit_amount,
    #         )
    
    # def process_subscription(self):
    #     """
    #     Process 'customer.subscription.created', 'customer.subscription.paused' or 'customer.subscription.deleted' events from Stripe.
    #     """
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No subscription data in event payload.")

    #     stripe_subscription_id = data.get('id')
    #     customer_id = data.get('customer')

    #     # Retrieve the associated Product using the Stripe customer ID
    #     customer = Account.objects.filter(stripe_customer_id=customer_id).first()
    #     if not customer:
    #         raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")


    #     # Check if the subscription exists
    #     subscription = Subscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()
    #     if subscription:
    #         # Update the existing subscription
    #         print(f"Subscription already exists with Stripe ID: {stripe_subscription_id}")
    #         subscription.customer = customer
    #         subscription.save()  # This will automatically call update_stripe_subscription
    #     else:
    #         # Create a new subscription
    #         print(f"Creating new subscription with Stripe ID: {stripe_subscription_id}")
    #         Subscription.objects.create(
    #             stripe_subscription_id=stripe_subscription_id,
    #             customer=customer,
    #         )

def process_subscription(self):
    """
    Process 'customer.subscription.created', 'customer.subscription.paused', or 'customer.subscription.deleted' events from Stripe.
    """
    data = self.data.get('object', {})
    if not data:
        raise ValueError("No subscription data in event payload.")

    stripe_subscription_id = data.get('id')
    customer_id = data.get('customer')
    items_data = data.get('items', {}).get('data', [])

    # Retrieve the associated Account using the Stripe customer ID
    customer = Account.objects.filter(stripe_customer_id=customer_id).first()
    if not customer:
        raise ValueError(f"Account with Stripe customer ID {customer_id} not found.")

    # Check if the subscription exists
    subscription, created = Subscription.objects.get_or_create(
        stripe_subscription_id=stripe_subscription_id,
        customer=customer
    )

    if created:
        print(f"Created new subscription with Stripe ID: {stripe_subscription_id}")
    else:
        print(f"Subscription already exists with Stripe ID: {stripe_subscription_id}")

    # Process subscription items
    for item_data in items_data:
        price_id = item_data.get('price', {}).get('id')
        quantity = item_data.get('quantity', 1)

        if not price_id:
            continue

        # Add or update subscription item
        subscription.add_item(price_id, quantity)

    def process_customer(self):
        """
        Process 'customer.created' or 'customer.updated' events from Stripe.
        """
        data = self.data.get('object', {})
        if not data:
            raise ValueError("No customer data in event payload.")

        stripe_customer_id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        description = data.get('description', '')

        # First, check if an account exists with the provided Stripe customer ID
        customer = Account.objects.filter(stripe_customer_id=stripe_customer_id).first()

        if customer:
            # Update the existing account
            print(f"Updating existing account with Stripe ID: {stripe_customer_id}")
            customer.name = name
            customer.email = email
            customer.description = description
            customer.save()  # This will automatically call `update_stripe_customer`
        else:
            # Check if an account with the same email already exists
            customer = Account.objects.filter(email=email).first()

            if customer:
                # Link the existing account with the Stripe customer ID
                print(f"Linking existing account with email {email} to Stripe ID: {stripe_customer_id}")
                customer.stripe_customer_id = stripe_customer_id
                customer.save()
            else:
                # Create a new account if none exists
                print(f"Creating new account with Stripe ID: {stripe_customer_id}")
                Account.objects.create(
                    stripe_customer_id=stripe_customer_id,
                    name=name,
                    username=email,
                    email=email,
                    description=description
                )





    # def process_customer(self):
    #     """
    #     Process 'customer.created' or 'customer.updated' events from Stripe.
    #     """
    #     data = self.data.get('object', {})
    #     if not data:
    #         raise ValueError("No customer data in event payload.")

    #     stripe_customer_id = data.get('id')
    #     name = data.get('name') or "Unnamed Customer"  # Default if name is None
    #     email = data.get('email')
    #     description = data.get('description', '')

    #     if not email:
    #         raise ValueError("Email is required for customer creation.")

    #     # Check if the customer exists
    #     customer = Account.objects.filter(stripe_customer_id=stripe_customer_id).first()
    #     if customer:
    #         # Update the existing customer
    #         print(f"Account already exists with Stripe ID: {stripe_customer_id}")
    #         customer.name = name
    #         customer.email = email
    #         customer.description = description
    #         customer.save()
    #     else:
    #         # Create a new customer
    #         print(f"Creating new customer with Stripe ID: {stripe_customer_id}")
    #         new_customer = Account(
    #             stripe_customer_id=stripe_customer_id,
    #             username=email,  # Use email as the default username
    #             name=name,
    #             email=email,
    #             description=description,
    #         )
    #         new_customer.save()  # Ensure save completes before further processing


    def process_customer_deleted(self):
        data = self.data.get('object', {})
        stripe_customer_id = data.get('id')
        customer = Account.objects.filter(stripe_customer_id=stripe_customer_id).first()
        if customer:
            customer.delete()
            print(f"Deleted customer with Stripe ID: {stripe_customer_id}")


    


