from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ...models import PaymentLink, PaymentLinkLineItem
from ...config.config import stripe


# def get_or_create_stripe_subscription(subscription):
#     """
#     Check if a Stripe subscription exists or create a new one.
#     """
#     try:
#         if subscription.stripe_subscription_id:
#             # Retrieve existing Stripe subscription
#             stripe_subscription = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
#             print(f"Found existing Stripe subscription: {stripe_subscription['id']}")
#             return stripe_subscription
#         else:
#             # Create a new Stripe subscription
#             items = [
#                 {
#                     "price": item.price.stripe_price_id,
#                     "quantity": item.quantity
#                 } for item in subscription.subscriptions.all()
#             ]
#             stripe_subscription = stripe.Subscription.create(
#                 customer=subscription.customer.stripe_customer_id,
#                 items=items
#             )
#             subscription.stripe_subscription_id = stripe_subscription["id"]
#             subscription.save()
#             print(f"Created new Stripe subscription: {stripe_subscription['id']}")
#             return stripe_subscription
#     except Exception as e:
#         print(f"Error in get_or_create_stripe_subscription: {e}")
#         raise

# @receiver(post_save, sender=Subscription)
# def create_or_update_stripe_subscription(sender, instance, created, **kwargs):
#     """
#     Create or update the Stripe subscription when a Subscription is saved.
#     """
#     try:
#         if created:
#             # Create a new Stripe subscription
#             stripe_subscription = get_or_create_stripe_subscription(instance)
#             print(f"Stripe subscription created: {stripe_subscription['id']}")
#         else:
#             # Update the existing Stripe subscription
#             if instance.stripe_subscription_id:
#                 items = [
#                     {
#                         "price": item.price.stripe_price_id,
#                         "quantity": item.quantity
#                     } for item in instance.subscriptions.all()
#                 ]
#                 stripe.Subscription.modify(
#                     instance.stripe_subscription_id,
#                     items=items
#                 )
#                 print(f"Updated Stripe subscription: {instance.stripe_subscription_id}")
#     except Exception as e:
#         print(f"Error syncing Stripe subscription: {e}")

# @receiver(post_save, sender=Subscription)
# def create_or_update_stripe_subscription(sender, instance, created, **kwargs):
#     """
#     Create or update the Stripe subscription when a Subscription is saved.
#     """
#     try:
#         items = [
#             {
#                 "price": item.price.stripe_price_id,
#                 "quantity": item.quantity
#             } for item in instance.subscription_items.all()
#         ]
#         if created:
#             # Create a new Stripe subscription
#             stripe_subscription = instance.create_or_update_stripe_subscription()
#             print(f"Stripe subscription created: {stripe_subscription['id']}")
#         else:
#             # Update the existing Stripe subscription
#             if instance.stripe_subscription_id:
#                 stripe.Subscription.modify(
#                     instance.stripe_subscription_id,
#                     items=items
#                 )
#                 print(f"Updated Stripe subscription: {instance.stripe_subscription_id}")
#     except Exception as e:
#         print(f"Error syncing Stripe subscription: {e}")

@receiver(post_save, sender=PaymentLink)
def handle_payment_link_post_save(sender, instance, created, **kwargs):
    """
    Handle post-save logic for PaymentLink to synchronize items with Stripe.
    """
    try:
        # Fetch related PaymentLinkLineItems after the PaymentLink is saved
        items = [
            {
                "price": item.price.stripe_price_id,
                "quantity": item.quantity
            } for item in instance.payment_link_line_items.all()
        ]

        print(f"post_save items: {items}")
        print(f"post_save instance.payment_link_line_items.all(): {instance.payment_link_line_items.all()}")

        if not items:
            print("No items to sync with Stripe.")
            return

        # Create or update Stripe payment_link
        stripe_payment_link = instance.create_or_update_stripe_payment_link()
        print(f"Stripe payment_link synced: {stripe_payment_link['id']}")
    except Exception as e:
        print(f"Error in post_save signal for PaymentLink: {e}")


@receiver(post_delete, sender=PaymentLink)
def delete_stripe_payment_link(sender, instance, **kwargs):
    """
    Delete the Stripe payment_link when a PaymentLink is deleted.
    """
    if instance.stripe_payment_link_id:
        try:
            stripe.PaymentLink.delete(instance.stripe_payment_link_id)
            print(f"Deleted Stripe payment_link: {instance.stripe_payment_link_id}")
        except Exception as e:
            print(f"Error deleting Stripe payment_link: {e}")

# @receiver(post_save, sender=SubscriptionItem)
# def update_subscription_items(sender, instance, created, **kwargs):
#     """
#     Update Stripe subscription items when a SubscriptionItem is added or updated.
#     """
#     try:
#         subscription = instance.subscription
#         if subscription and subscription.stripe_subscription_id:
#             items = [
#                 {
#                     "price": item.price.stripe_price_id,
#                     "quantity": item.quantity
#                 } for item in subscription.subscriptions.all()
#             ]
#             stripe.Subscription.modify(
#                 subscription.stripe_subscription_id,
#                 items=items
#             )
#             print(f"Updated Stripe subscription items for: {subscription.stripe_subscription_id}")
#     except Exception as e:
#         print(f"Error updating Stripe subscription items: {e}")

@receiver(post_save, sender=PaymentLinkLineItem)
def update_payment_link_line_items(sender, instance, created, **kwargs):
    """
    Update Stripe payment_link items when a PaymentLinkLineItem is added or updated.
    """
    try:
        payment_link = instance.payment_link
        if payment_link and payment_link.stripe_payment_link_id:
            items = [
                {
                    "price": item.price.stripe_price_id,
                    "quantity": item.quantity
                } for item in payment_link.payment_link_line_items.all()
            ]
            stripe.PaymentLink.modify(
                payment_link.stripe_payment_link_id,
                items=items
            )
            print(f"Updated Stripe payment_link items for: {payment_link.stripe_payment_link_id}")
    except Exception as e:
        print(f"Error updating Stripe payment_link items: {e}")


@receiver(post_delete, sender=PaymentLinkLineItem)
def remove_payment_link_line_item(sender, instance, **kwargs):
    """
    Update Stripe payment_link when a PaymentLinkLineItem is deleted.
    """
    try:
        payment_link = instance.payment_link
        if payment_link and payment_link.stripe_payment_link_id:
            items = [
                {
                    "price": item.price.stripe_price_id,
                    "quantity": item.quantity
                } for item in payment_link.payment_links.all() if item.id != instance.id
            ]
            stripe.PaymentLink.modify(
                payment_link.stripe_payment_link_id,
                items=items
            )
            print(f"Updated Stripe payment_link after item removal: {payment_link.stripe_payment_link_id}")
    except Exception as e:
        print(f"Error updating Stripe payment_link after item removal: {e}")
