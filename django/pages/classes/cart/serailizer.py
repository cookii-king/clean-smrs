from rest_framework import serializers
from ...models import Cart, CartItem, Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product to include relevant details in the cart item serialization.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stripe_product_id']  # Adjust fields as needed.

class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem, includes related product details.
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        """
        Calculate total price for the cart item based on quantity.
        """
        return obj.product.price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart, includes related cart items.
    """
    items = CartItemSerializer(many=True, read_only=True, source='items')  # 'items' is the related_name in the Cart model.

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        """
        Calculate total price for the entire cart.
        """
        return sum(item.product.price * item.quantity for item in obj.items.all())
