from django.contrib import admin
from .models import Account, Plan, Price, Product, Subscription

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'email_confirmed', 'mfa_enabled', 'created', 'updated')
    search_fields = ('username', 'email', 'name')
    list_filter = ('email_confirmed', 'mfa_enabled', 'created')
    readonly_fields = ('created', 'updated')

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'interval', 'product', 'amount', 'stripe_plan_id', 'created', 'updated', 'deleted')
    search_fields = ('product', 'stripe_plan_id', 'currency')
    list_filter = ('currency', 'interval', 'created', 'deleted')
    readonly_fields = ('created', 'updated')

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'product', 'unit_amount', 'stripe_price_id', 'created', 'updated', 'deleted')
    search_fields = ('product', 'stripe_price_id', 'currency')
    list_filter = ('currency', 'created', 'updated', 'deleted')
    readonly_fields = ('created', 'updated')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'stripe_product_id', 'created', 'updated', 'deleted')
    search_fields = ('name', 'stripe_product_id', 'description')
    list_filter = ('created', 'updated', 'deleted')
    readonly_fields = ('created', 'updated')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'stripe_subscription_id', 'created', 'updated', 'deleted')
    search_fields = ('customer', 'stripe_subscription_id')
    list_filter = ('created', 'updated', 'deleted')
    readonly_fields = ('created', 'updated')