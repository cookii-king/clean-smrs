from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ...models import Price, Product, ProductImage
from ...config.config import stripe
import urllib.parse


def get_or_create_stripe_price(price):
    """
    Check if a Stripe price with the given details exists.
    If it exists, return the existing price. Otherwise, create a new one.
    """
    try:
        if price.stripe_price_id:
            # Retrieve existing Stripe price
            stripe_price = stripe.Price.retrieve(price.stripe_price_id)
            print(f"Found existing Stripe price: {stripe_price['id']}")
            return stripe_price
        else:
            # Convert amount to cents (Stripe expects amounts in cents)
            amount_in_cents = int(price.unit_amount * 100)
            
            # Create a new price in Stripe
            stripe_price = stripe.Price.create(
                unit_amount=amount_in_cents,
                currency=price.currency,
                recurring=price.recurring if price.recurring else None,
                product=price.product.stripe_product_id,
            )
            price.stripe_price_id = stripe_price["id"]
            price.save()
            print(f"Created new Stripe price: {stripe_price['id']}")
            return stripe_price
    except Exception as e:
        print(f"Error in get_or_create_stripe_price: {e}")
        raise


@receiver(post_save, sender=Price)
def create_stripe_price(sender, instance, created, **kwargs):
    """
    Create or synchronize the Stripe price after saving the Price model.
    """
    try:
        if created and not instance.stripe_price_id:
            stripe_price = get_or_create_stripe_price(instance)
            instance.stripe_price_id = stripe_price["id"]
            instance.save()
            print(f"Stripe price created: {stripe_price['id']}")
    except Exception as e:
        print(f"Error creating Stripe price: {e}")


@receiver(post_save, sender=Price)
def sync_stripe_price(sender, instance, created, **kwargs):
    """
    Update the Stripe price when the Price model is updated.
    """
    try:
        if not created and instance.stripe_price_id:
            stripe.Price.modify(
                instance.stripe_price_id,
                product=instance.product.stripe_product_id,
            )
            print(f"Updated Stripe price: {instance.stripe_price_id}")
    except Exception as e:
        print(f"Error syncing Stripe price: {e}")


@receiver(post_delete, sender=Price)
def delete_stripe_price(sender, instance, **kwargs):
    """
    Delete the Stripe price when the Price model is deleted.
    """
    try:
        if instance.stripe_price_id:
            stripe.Price.delete(instance.stripe_price_id)
            print(f"Deleted Stripe price: {instance.stripe_price_id}")
    except Exception as e:
        print(f"Error deleting Stripe price: {e}")
