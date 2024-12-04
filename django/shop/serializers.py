from rest_framework import serializers
from .models import Order, Product, Cart, Subscription, SubscriptionPlan

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # fields = ['id', 'account_id', 'order_date', 'total_amount', 'status']
        fields = ['id', 'account_id', 'order_date', 'status']
        extra_kwargs = {
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'status']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'account_id', 'products']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        # fields = ['id', 'account_id', 'plan_id', 'status']
        fields = ['id', 'account_id', 'status']
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance