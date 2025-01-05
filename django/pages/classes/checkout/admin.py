from django.contrib import admin
from django import forms
from ...config.config import stripe
from ...models import Checkout, CheckoutLineItem, Account, Price

class CheckoutAdminForm(forms.ModelForm):
    """
    Custom form for managing Checkouts in the admin interface.
    """
    # customer = forms.ModelChoiceField(
    #     queryset=Account.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     label="Customer",
    #     required=True
    # )

    class Meta:
        model = Checkout
        # fields = ['customer']
        fields = []

    def save(self, commit=True):
        """
        Override save to link the customer to the checkout.
        """
        instance = super().save(commit=False)
        print(f"override save items: ${instance.checkout_line_items.all()}")
        if commit:
            instance.save()
        return instance

class CheckoutLineItemInline(admin.TabularInline):
    """
    Inline for managing CheckoutLineItem instances related to a Checkout.
    """
    model = CheckoutLineItem
    extra = 1
    fields = ('price', 'quantity')
    autocomplete_fields = ['price']  # Enables search for prices in the admin

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Checkout.
    """
    form = CheckoutAdminForm
    list_display = ('id', 'created', 'updated', 'deleted')
    # search_fields = ('id', 'customer__stripe_customer_id')
    list_filter = ('created', 'updated', 'deleted')
    readonly_fields = ('id', 'created', 'updated')
    inlines = [CheckoutLineItemInline]

    def save_model(self, request, obj, form, change):
        """
        Save the Checkout instance. Don't sync items here since they aren't saved yet.
        """
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """
        Save related CheckoutLineItems and synchronize with Stripe after all items are saved.
        """
        super().save_related(request, form, formsets, change)

        # Now that all related objects are saved, sync with Stripe
        checkout = form.instance
        try:
            items = [
                {
                    "price": item.price.stripe_price_id,
                    "quantity": item.quantity
                } for item in checkout.checkout_line_items.all()
            ]

            print(f"save_related items: {items}")
            print(f"save_related checkout.checkout_line_items.all(): {checkout.checkout_line_items.all()}")

            if not items:
                self.message_user(request, "No items associated with this checkout.", level='warning')
                return

            # Create or update Stripe checkout
            stripe_checkout = checkout.create_or_update_stripe_checkout()
            self.message_user(request, f"Stripe checkout synced: {stripe_checkout['id']}")
        except Exception as e:
            self.message_user(request, f"Error syncing Stripe checkout: {e}", level='error')


# class SubscriptionItemInline(admin.TabularInline):
#     """
#     Inline for managing SubscriptionItem instances related to a Subscription.
#     """
#     model = SubscriptionItem
#     extra = 1
#     fields = ('price', 'quantity')  # Explicitly define fields to avoid issues


# @admin.register(Subscription)
# class SubscriptionAdmin(admin.ModelAdmin):
#     """
#     Admin interface for managing Subscriptions.
#     """
#     list_display = ('id', 'customer', 'created', 'updated', 'deleted')
#     search_fields = ('id', 'customer__stripe_customer_id')
#     list_filter = ('created', 'updated', 'deleted')
#     readonly_fields = ('id', 'created', 'updated')
#     inlines = [SubscriptionItemInline]

#     def save_model(self, request, obj, form, change):
#         """
#         Override save_model to synchronize Stripe subscription when saving.
#         """
#         super().save_model(request, obj, form, change)  # Save the Subscription
#         try:
#             # Build the items list for Stripe
#             items = [
#                 {
#                     "price": item.price.stripe_price_id,
#                     "quantity": item.quantity
#                 } for item in obj.subscription_items.all()
#             ]

#             if not items:
#                 self.message_user(request, "No items associated with this subscription.", level='warning')
#                 return

#             # Create or update Stripe subscription
#             stripe_subscription = obj.create_or_get_stripe_subscription(items=items)
#             self.message_user(request, f"Stripe subscription synced: {stripe_subscription['id']}")
#         except Exception as e:
#             self.message_user(request, f"Error syncing Stripe subscription: {e}", level='error')

#     def delete_model(self, request, obj):
#         """
#         Override delete_model to delete associated Stripe subscription.
#         """
#         try:
#             if obj.stripe_subscription_id:
#                 obj.delete_stripe_subscription()
#                 self.message_user(request, f"Deleted Stripe subscription: {obj.stripe_subscription_id}")
#         except Exception as e:
#             self.message_user(request, f"Error deleting Stripe subscription: {e}", level='error')
#         super().delete_model(request, obj)


# class SubscriptionItemAdminForm(forms.ModelForm):
#     """
#     Custom form for validating SubscriptionItem data in the admin.
#     """
#     class Meta:
#         model = SubscriptionItem
#         fields = '__all__'

#     def clean(self):
#         """
#         Custom validation for SubscriptionItem.
#         """
#         cleaned_data = super().clean()
#         quantity = cleaned_data.get('quantity')

#         if quantity is not None and quantity <= 0:
#             raise forms.ValidationError("Quantity must be greater than zero.")

#         return cleaned_data


# @admin.register(SubscriptionItem)
# class SubscriptionItemAdmin(admin.ModelAdmin):
#     """
#     Admin interface for managing Subscription Items.
#     """
#     list_display = ('subscription', 'price', 'quantity')
#     search_fields = ('subscription__id', 'price__stripe_price_id')
#     list_filter = ('subscription',)
#     form = SubscriptionItemAdminForm

# # from django.contrib import admin
# # from django import forms
# # from ...models import Subscription, SubscriptionItem
# # from array import *
# # from django.contrib import admin
# # from django import forms
# # from django.db.models.signals import post_save
# # from django.dispatch import receiver
# # from ...models import Subscription, SubscriptionItem

# # # class SubscriptionItemInline(admin.TabularInline):
# # #     """
# # #     Inline for managing SubscriptionItem instances related to a Subscription.
# # #     """
# # #     model = SubscriptionItem
# # #     extra = 1  # Number of empty forms to display for adding new items

# # class SubscriptionItemInline(admin.TabularInline):
# #     model = SubscriptionItem
# #     extra = 1
# #     fields = ('price', 'quantity')  # Explicitly define fields to avoid issues



# # @admin.register(Subscription)
# # class SubscriptionAdmin(admin.ModelAdmin):
# #     list_display = ('id', 'customer', 'created', 'updated', 'deleted')
# #     search_fields = ('id',  'customer_id')
# #     list_filter = ('created', 'updated', 'deleted')
# #     readonly_fields = ('id', 'created', 'updated', )
# #     inlines = [SubscriptionItemInline]  # Inline for related subscription items

# #     def save_model(self, request, obj, form, change):
# #         """
# #         Override save_model to save the Subscription first,
# #         then fetch related SubscriptionItems for Stripe API call.
# #         """
# #         super().save_model(request, obj, form, change)  # Save the Subscription
# #         try:
# #             # Fetch related SubscriptionItems after saving
# #             # items = [
# #             #     {
# #             #         "price": item.price.stripe_price_id,
# #             #         "quantity": item.quantity
# #             #     } for item in obj.subscriptions.all()
# #             # ]
# #             items = [{"price": "price_1QctesLqX3boq1N3xigIBPeC"}]
# #             print(f"obj.subscription_items.all(): ${obj.subscription_items.all()}")
# #             for i in obj.subscription_items.all():
# #                 print(f"i: ${i}") 
# #                 items.append(i)
# #             if not items:
# #                 self.message_user(request, "No items associated with this subscription.", level='warning')
# #                 return
# #             print(f"admin items: ${items}") 

# #             # Create or update Stripe subscription
# #             stripe_subscription = obj.create_or_get_stripe_subscription(items)
# #             self.message_user(request, f"Stripe subscription synced: {stripe_subscription['id']}")
# #         except Exception as e:
# #             self.message_user(request, f"Error syncing Stripe subscription: {e}", level='error')

# #     def delete_model(self, request, obj):
# #         """
# #         Override delete_model to delete associated Stripe subscription.
# #         """
# #         try:
# #             if obj.stripe_subscription_id:
# #                 obj.delete_stripe_subscription()
# #                 self.message_user(request, f"Deleted Stripe subscription: {obj.stripe_subscription_id}")
# #         except Exception as e:
# #             self.message_user(request, f"Error deleting Stripe subscription: {e}", level='error')
# #         super().delete_model(request, obj)

# # class SubscriptionItemAdminForm(forms.ModelForm):
# #     class Meta:
# #         model = SubscriptionItem
# #         fields = '__all__'

# #     def clean(self):
# #         cleaned_data = super().clean()
# #         quantity = cleaned_data.get('quantity')
# #         if quantity <= 0:
# #             raise forms.ValidationError("Quantity must be greater than zero.")
# #         return cleaned_data

# # @admin.register(SubscriptionItem)
# # class SubscriptionItemAdmin(admin.ModelAdmin):
# #     list_display = ('subscription', 'price', 'quantity')
# #     search_fields = ('subscription__id', 'price__stripe_price_id')
# #     list_filter = ('subscription',)
# #     form = SubscriptionItemAdminForm
