# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from ...models import Checkout, CheckoutLineItem
# from ...config.config import stripe


# # def get_or_create_stripe_subscription(subscription):
# #     """
# #     Check if a Stripe subscription exists or create a new one.
# #     """
# #     try:
# #         if subscription.stripe_subscription_id:
# #             # Retrieve existing Stripe subscription
# #             stripe_subscription = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
# #             print(f"Found existing Stripe subscription: {stripe_subscription['id']}")
# #             return stripe_subscription
# #         else:
# #             # Create a new Stripe subscription
# #             items = [
# #                 {
# #                     "price": item.price.stripe_price_id,
# #                     "quantity": item.quantity
# #                 } for item in subscription.subscriptions.all()
# #             ]
# #             stripe_subscription = stripe.Subscription.create(
# #                 customer=subscription.customer.stripe_customer_id,
# #                 items=items
# #             )
# #             subscription.stripe_subscription_id = stripe_subscription["id"]
# #             subscription.save()
# #             print(f"Created new Stripe subscription: {stripe_subscription['id']}")
# #             return stripe_subscription
# #     except Exception as e:
# #         print(f"Error in get_or_create_stripe_subscription: {e}")
# #         raise

# # @receiver(post_save, sender=Subscription)
# # def create_or_update_stripe_subscription(sender, instance, created, **kwargs):
# #     """
# #     Create or update the Stripe subscription when a Subscription is saved.
# #     """
# #     try:
# #         if created:
# #             # Create a new Stripe subscription
# #             stripe_subscription = get_or_create_stripe_subscription(instance)
# #             print(f"Stripe subscription created: {stripe_subscription['id']}")
# #         else:
# #             # Update the existing Stripe subscription
# #             if instance.stripe_subscription_id:
# #                 items = [
# #                     {
# #                         "price": item.price.stripe_price_id,
# #                         "quantity": item.quantity
# #                     } for item in instance.subscriptions.all()
# #                 ]
# #                 stripe.Subscription.modify(
# #                     instance.stripe_subscription_id,
# #                     items=items
# #                 )
# #                 print(f"Updated Stripe subscription: {instance.stripe_subscription_id}")
# #     except Exception as e:
# #         print(f"Error syncing Stripe subscription: {e}")

# # @receiver(post_save, sender=Subscription)
# # def create_or_update_stripe_subscription(sender, instance, created, **kwargs):
# #     """
# #     Create or update the Stripe subscription when a Subscription is saved.
# #     """
# #     try:
# #         items = [
# #             {
# #                 "price": item.price.stripe_price_id,
# #                 "quantity": item.quantity
# #             } for item in instance.subscription_items.all()
# #         ]
# #         if created:
# #             # Create a new Stripe subscription
# #             stripe_subscription = instance.create_or_update_stripe_subscription()
# #             print(f"Stripe subscription created: {stripe_subscription['id']}")
# #         else:
# #             # Update the existing Stripe subscription
# #             if instance.stripe_subscription_id:
# #                 stripe.Subscription.modify(
# #                     instance.stripe_subscription_id,
# #                     items=items
# #                 )
# #                 print(f"Updated Stripe subscription: {instance.stripe_subscription_id}")
# #     except Exception as e:
# #         print(f"Error syncing Stripe subscription: {e}")

# @receiver(post_save, sender=Checkout)
# def handle_checkout_post_save(sender, instance, created, **kwargs):
#     """
#     Handle post-save logic for Checkout to synchronize items with Stripe.
#     """
#     try:
#         # # Fetch related CheckoutLineItem after the Checkout is saved
#         # items = [
#         #     {
#         #         "price": item.price.stripe_price_id,
#         #         "quantity": item.quantity
#         #     } for item in instance.checkout_line_items.all()
#         # ]

#         items = []

#         # Iterate through all checkout items and add to the items list
#         for item in instance.get_items():
#             if item.price:
#                 stripe_id = item.price.stripe_price_id
#             elif item.plan:
#                 stripe_id = item.plan.stripe_plan_id
#             else:
#                 raise ValueError("CheckoutLineItem must have either a price or a plan.")

#             items.append({
#                 "price": stripe_id,
#                 "quantity": item.quantity
#             })
        
#         print(f"signal items: {items}")
#         print(f"post_save items: {items}")
#         print(f"post_save instance.checkout_line_items.all(): {instance.checkout_line_items.all()}")

#         if not items:
#             print("No items to sync with Stripe.")
#             return

#         # Create or update Stripe checkout
#         stripe_checkout = instance.create_or_update_stripe_checkout()
#         print(f"Stripe checkout synced: {stripe_checkout['id']}")
#     except Exception as e:
#         print(f"Error in post_save signal for Checkout: {e}")


# @receiver(post_delete, sender=Checkout)
# def delete_stripe_checkout(sender, instance, **kwargs):
#     """
#     Delete the Stripe checkout when a Checkout is deleted.
#     """
#     if instance.stripe_checkout_id:
#         try:
#             stripe.checkout.Session.delete(instance.stripe_checkout_id)
#             print(f"Deleted Stripe checkout: {instance.stripe_checkout_id}")
#         except Exception as e:
#             print(f"Error deleting Stripe checkout: {e}")

# # @receiver(post_save, sender=SubscriptionItem)
# # def update_subscription_items(sender, instance, created, **kwargs):
# #     """
# #     Update Stripe subscription items when a SubscriptionItem is added or updated.
# #     """
# #     try:
# #         subscription = instance.subscription
# #         if subscription and subscription.stripe_subscription_id:
# #             items = [
# #                 {
# #                     "price": item.price.stripe_price_id,
# #                     "quantity": item.quantity
# #                 } for item in subscription.subscriptions.all()
# #             ]
# #             stripe.Subscription.modify(
# #                 subscription.stripe_subscription_id,
# #                 items=items
# #             )
# #             print(f"Updated Stripe subscription items for: {subscription.stripe_subscription_id}")
# #     except Exception as e:
# #         print(f"Error updating Stripe subscription items: {e}")

# @receiver(post_save, sender=CheckoutLineItem)
# def update_checkout_line_items(sender, instance, created, **kwargs):
#     """
#     Update Stripe checkout items when a CheckoutLineItem is added or updated.
#     """
#     try:
#         checkout = instance.checkout
#         if checkout and checkout.stripe_checkout_id:
#             # items = [
#             #     {
#             #         "price": item.price.stripe_price_id,
#             #         "quantity": item.quantity
#             #     } for item in checkout.checkout_line_items.all()
#             # ]
#             items = []

#             # Iterate through all checkout items and add to the items list
#             for item in instance.get_items():
#                 if item.price:
#                     stripe_id = item.price.stripe_price_id
#                 elif item.plan:
#                     stripe_id = item.plan.stripe_plan_id
#                 else:
#                     raise ValueError("CheckoutLineItem must have either a price or a plan.")

#                 items.append({
#                     "price": stripe_id,
#                     "quantity": item.quantity
#                 })
            
#             print(f"signal items: {items}")
#             stripe.checkout.Session.modify(
#                 checkout.stripe_checkout_id,
#                 line_items=items
#             )
#             print(f"Updated Stripe checkout items for: {checkout.stripe_checkout_id}")
#     except Exception as e:
#         print(f"Error updating Stripe checkout items: {e}")


# @receiver(post_delete, sender=CheckoutLineItem)
# def remove_checkout_line_item(sender, instance, **kwargs):
#     """
#     Update Stripe checkout when a CheckoutLineItem is deleted.
#     """
#     try:
#         checkout = instance.checkout
#         if checkout and checkout.stripe_checkout_id:
#             # items = [
#             #     {
#             #         "price": item.price.stripe_price_id,
#             #         "quantity": item.quantity
#             #     } for item in checkout.checkouts.all() if item.id != instance.id
#             # ]
#             items = []

#             # Iterate through all checkout items and add to the items list
#             for item in instance.get_items():
#                 if item.price:
#                     stripe_id = item.price.stripe_price_id
#                 elif item.plan:
#                     stripe_id = item.plan.stripe_plan_id
#                 else:
#                     raise ValueError("CheckoutLineItem must have either a price or a plan.")

#                 items.append({
#                     "price": stripe_id,
#                     "quantity": item.quantity
#                 })
            
#             print(f"signal items: {items}")

#             stripe.checkout.Session.modify(
#                 checkout.stripe_checkout_id,
#                 line_items=items
#             )
#             print(f"Updated Stripe checkout after item removal: {checkout.stripe_checkout_id}")
#     except Exception as e:
#         print(f"Error updating Stripe checkout after item removal: {e}")
