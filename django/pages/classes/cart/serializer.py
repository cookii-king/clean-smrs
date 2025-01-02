# django/pages/classes/cart/serializer.py

from rest_framework import serializers
from pages.classes.product.serializer import ProductSerializer
from pages.classes.cart.model import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem, includes related product details.
    """
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart, includes related cart items.
    """
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created', 'updated']
