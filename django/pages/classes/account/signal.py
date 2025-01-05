from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from ...models import Account
from ...config.config import stripe


def get_or_create_stripe_customer(email):
    """
    Check if a Stripe customer with the given email already exists.
    If it exists, return the existing customer. Otherwise, create a new one.
    """
    try:
        # Search for a Stripe customer with the given email
        customers = stripe.Customer.list(email=email).data
        if customers:
            print(f"Found existing Stripe customer for email: {email}")
            return customers[0]
        else:
            # Create a new Stripe customer
            stripe_customer = stripe.Customer.create(email=email)
            print(f"Created new Stripe customer for email: {email}")
            return stripe_customer
    except Exception as e:
        print(f"Error in get_or_create_stripe_customer: {e}")
        raise


@receiver(post_save, sender=Account)
def handle_stripe_customer(sender, instance, created, **kwargs):
    """
    Handle Stripe customer creation or update after saving an Account.
    """
    if hasattr(instance, '_disable_post_save'):
        return  # Prevent recursive signal handling

    try:
        if created and not instance.stripe_customer_id:
            # Create a new Stripe customer
            stripe_customer = get_or_create_stripe_customer(instance.email)
            instance.stripe_customer_id = stripe_customer["id"]

            # Temporarily disable post_save to prevent recursion
            instance._disable_post_save = True
            instance.save()
            del instance._disable_post_save  # Clean up the temporary flag
        elif not created and instance.stripe_customer_id:
            # Update the existing Stripe customer
            stripe.Customer.modify(
                instance.stripe_customer_id,
                email=instance.email,
                name=instance.name,
            )
            print(f"Updated Stripe customer: {instance.stripe_customer_id}")
    except Exception as e:
        print(f"Error handling Stripe customer: {e}")


@receiver(post_delete, sender=Account)
def delete_stripe_customer(sender, instance, **kwargs):
    """
    Delete the Stripe customer when an account is deleted.
    """
    if instance.stripe_customer_id:
        try:
            stripe.Customer.delete(instance.stripe_customer_id)
            print(f"Deleted Stripe customer: {instance.stripe_customer_id}")
        except Exception as e:
            print(f"Error deleting Stripe customer: {e}")


@receiver(pre_delete, sender=Account)
def prevent_last_admin_deletion(sender, instance, **kwargs):
    """
    Prevent deletion of the last admin account.
    """
    if instance.is_superuser and Account.objects.filter(is_superuser=True).count() == 1:
        raise ValueError("Cannot delete the last admin account.")


@receiver(pre_save, sender=Account)
def prevent_removing_last_admin_privileges(sender, instance, **kwargs):
    """
    Prevent removing admin privileges from the last admin account.
    """
    if not instance.pk:  # New instance, no admin privileges to check
        return

    try:
        current_instance = Account.objects.get(pk=instance.pk)
        if current_instance.is_superuser and not instance.is_superuser:
            # Ensure this is not the last admin
            if Account.objects.filter(is_superuser=True).exclude(pk=instance.pk).count() == 0:
                raise ValueError("Cannot remove admin privileges from the last admin account.")
    except Account.DoesNotExist:
        # Instance is new, no need to check
        pass
