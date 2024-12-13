# from django.contrib import admin
# from .models import Product, ProductMedia


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'price', 'status', 'created', 'updated')
#     search_fields = ('name', 'category')
#     list_filter = ('category', 'status')


# admin.site.register(Product)

# class ProductMediaAdmin(admin.ModelAdmin):
#     list_display = ('product', 'media_type', 'url', 'file', 'created')

# admin.site.register(ProductMedia)

from django.contrib import admin
from .models import Product, ProductMedia, Order, Cart, CartProduct, SubscriptionPlan, Subscription


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'status', 'created', 'updated')
    search_fields = ('name', 'category')
    list_filter = ('category', 'status')


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ('product', 'media_type', 'url', 'file', 'created')
    search_fields = ('product__name', 'media_type')
    list_filter = ('media_type',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_id', 'order_date', 'status', 'created', 'updated')
    search_fields = ('id', 'account__username', 'status')
    list_filter = ('status', 'order_date')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_id', 'created', 'updated')
    search_fields = ('id', 'account__username')


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__id', 'product__name')


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created', 'updated')
    search_fields = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_id', 'status', 'created', 'updated')
    search_fields = ('id', 'account__username', 'status')
    list_filter = ('status',)
