# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from ...models import Plan, Product, ProductImage
# from ...config.config import stripe
# import urllib.parse


# def get_or_create_stripe_plan(plan):
#     """
#     Check if a Stripe plan with the given details exists.
#     If it exists, return the existing plan. Otherwise, create a new one.
#     """
#     try:
#         if plan.stripe_plan_id:
#             # Retrieve existing Stripe plan
#             stripe_plan = stripe.Plan.retrieve(plan.stripe_plan_id)
#             print(f"Found existing Stripe plan: {stripe_plan['id']}")
#             return stripe_plan
#         else:
#             # Create a new plan in Stripe
#             stripe_plan = stripe.Plan.create(
#                 amount=plan.amount,
#                 currency=plan.currency,
#                 interval=plan.interval,
#                 product=plan.product.stripe_product_id,
#             )
#             plan.stripe_plan_id = stripe_plan["id"]
#             plan.save()
#             print(f"Created new Stripe plan: {stripe_plan['id']}")
#             return stripe_plan
#     except Exception as e:
#         print(f"Error in get_or_create_stripe_plan: {e}")
#         raise


# @receiver(post_save, sender=Plan)
# def create_stripe_plan(sender, instance, created, **kwargs):
#     """
#     Create or synchronize the Stripe plan after saving the Plan model.
#     """
#     if created and not instance.stripe_plan_id:
#         try:
#             stripe_plan = get_or_create_stripe_plan(instance)
#             instance.stripe_plan_id = stripe_plan["id"]
#             instance.save()
#         except Exception as e:
#             print(f"Error creating Stripe plan: {e}")


# @receiver(post_save, sender=Plan)
# def sync_stripe_plan(sender, instance, created, **kwargs):
#     """
#     Update the Stripe plan when the Plan model is updated.
#     """
#     if not created and instance.stripe_plan_id:
#         try:
#             stripe.Plan.modify(
#                 instance.stripe_plan_id,
#                 product=instance.product.stripe_product_id,
#             )
#             print(f"Updated Stripe plan: {instance.stripe_plan_id}")
#         except Exception as e:
#             print(f"Error syncing Stripe plan: {e}")


# @receiver(post_delete, sender=Plan)
# def delete_stripe_plan(sender, instance, **kwargs):
#     """
#     Delete the Stripe plan when the Plan model is deleted.
#     """
#     if instance.stripe_plan_id:
#         try:
#             stripe.Plan.delete(instance.stripe_plan_id)
#             print(f"Deleted Stripe plan: {instance.stripe_plan_id}")
#         except Exception as e:
#             print(f"Error deleting Stripe plan: {e}")
