from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'status', 'created', 'updated')
    search_fields = ('name', 'category')
    list_filter = ('category', 'status')


admin.site.register(Product)
