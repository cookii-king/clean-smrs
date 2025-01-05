# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from ...models import Subscription, SubscriptionItem, ApiKey
# from ...config.config import stripe

# @receiver(post_save, sender=Subscription)
# def handle_subscription_post_save(sender, instance, created, **kwargs):
#     """
#     Handle post-save logic for Subscription to synchronize items with Stripe.
#     """
#     try:
#         items = [
#             {
#                 "price": item.price.stripe_price_id,
#                 "quantity": item.quantity
#             } for item in instance.subscription_items.all()
#         ]
#         if not items:
#             print("No items to sync with Stripe.")
#             return

#         # Create or update Stripe subscription
#         instance.create_or_update_stripe_subscription()
#         print(f"Stripe subscription synced: {instance.stripe_subscription_id}")
#     except Exception as e:
#         print(f"Error in post_save signal for Subscription: {e}")

# @receiver(post_delete, sender=Subscription)
# def delete_stripe_subscription(sender, instance, **kwargs):
#     """
#     Delete the Stripe subscription when a Subscription is deleted.
#     """
#     if instance.stripe_subscription_id:
#         try:
#             stripe.Subscription.delete(instance.stripe_subscription_id)
#             print(f"Deleted Stripe subscription: {instance.stripe_subscription_id}")
#         except Exception as e:
#             print(f"Error deleting Stripe subscription: {e}")

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
#                 } for item in subscription.subscription_items.all()
#             ]
#             stripe.Subscription.modify(
#                 subscription.stripe_subscription_id,
#                 items=items
#             )
#             print(f"Updated Stripe subscription items for: {subscription.stripe_subscription_id}")
#     except Exception as e:
#         print(f"Error updating Stripe subscription items: {e}")

# @receiver(post_delete, sender=SubscriptionItem)
# def remove_subscription_item(sender, instance, **kwargs):
#     """
#     Update Stripe subscription when a SubscriptionItem is deleted.
#     """
#     try:
#         subscription = instance.subscription
#         if subscription and subscription.stripe_subscription_id:
#             items = [
#                 {
#                     "price": item.price.stripe_price_id,
#                     "quantity": item.quantity
#                 } for item in subscription.subscription_items.all() if item.id != instance.id
#             ]
#             stripe.Subscription.modify(
#                 subscription.stripe_subscription_id,
#                 items=items
#             )
#             print(f"Updated Stripe subscription after item removal: {subscription.stripe_subscription_id}")
#     except Exception as e:
#         print(f"Error updating Stripe subscription after item removal: {e}")

# def ensure_single_api_key(account):
#     """
#     Ensure that there is only one active ApiKey per account.
#     """
#     api_keys = ApiKey.objects.filter(account=account)
#     if api_keys.count() > 1:
#         # Deactivate all but the most recent key
#         for api_key in api_keys.order_by('-created')[1:]:
#             api_key.active = False
#             api_key.save()

# # Example usage in your webhook or other logic
# def handle_api_key_creation(account):
#     api_key, created = ApiKey.objects.get_or_create(account=account)
#     if created:
#         print(f"New API key created for account {account.id}: {api_key.key}")
#         api_key.generate_key()
#     else:
#         print(f"Existing API key retrieved for account {account.id}: {api_key.key}")
#         api_key.active = True
#         api_key.save()

#     ensure_single_api_key(account)