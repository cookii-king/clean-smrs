from django.contrib import admin
from .models import User, Order, Product, OrderItem, Subscription, DataPoint


admin.site.register(User)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Subscription)
admin.site.register(DataPoint)
