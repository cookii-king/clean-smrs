from django.contrib import admin
from django import forms
from ...models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    """
    Inline for managing ProductImage instances related to a Product.
    """
    model = ProductImage
    extra = 1  # Number of empty forms to display for adding new images

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Product name is required.")
        return cleaned_data
    
    def clean_type(self):
        type_value = self.cleaned_data.get('type')
        if type_value not in ['product', 'service']:
            raise forms.ValidationError("Type must be 'product' or 'service'.")
        return type_value

    def clean_reoccurrence(self):
        reoccurrence_value = self.cleaned_data.get('reoccurrence')
        if reoccurrence_value not in ['one-time', 'reoccurring']:
            raise forms.ValidationError("Re-Occurrence must be 'one-time' or 'reoccurring'.")
        return reoccurrence_value


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'type', 'reoccurrence', 'description', 'stripe_product_id', 'created', 'updated')
    search_fields = ('name', 'type', 'reoccurrence', 'description')
    list_filter = ('type', 'reoccurrence', 'created', 'updated')
    readonly_fields = ('created', 'updated', 'stripe_product_id')
    inlines = [ProductImageInline]  # Inline for related images

    def save_model(self, request, obj, form, change):
        """
        Override save_model to create or update Stripe product when saving in admin.
        """
        super().save_model(request, obj, form, change)
        try:
            # Automatically create or update the Stripe product
            stripe_product = obj.create_or_get_stripe_product()
            self.message_user(request, f"Stripe product synced: {stripe_product['id']}")
        except Exception as e:
            self.message_user(request, f"Error syncing Stripe product: {e}", level='error')

    def delete_model(self, request, obj):
        """
        Override delete_model to delete associated Stripe product.
        """
        try:
            if obj.stripe_product_id:
                obj.delete_stripe_product()
                self.message_user(request, f"Deleted Stripe product: {obj.stripe_product_id}")
        except Exception as e:
            self.message_user(request, f"Error deleting Stripe product: {e}", level='error')
        super().delete_model(request, obj)

