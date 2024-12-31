from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ...models import Cart, CartItem, Product
from ...serializers import CartSerializer, CartItemSerializer

class CartView(APIView):
    """
    Manage cart actions such as retrieving, adding, updating, and removing items.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the user's cart and its items.
        """
        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": f"Failed to retrieve cart: {str(e)}"}, status=400)

    def post(self, request):
        """
        Add a product to the cart or update its quantity if it already exists.
        """
        try:
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)

            product = get_object_or_404(Product, id=product_id)
            cart, _ = Cart.objects.get_or_create(user=request.user)

            # Add or update the product in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += int(quantity)
            else:
                cart_item.quantity = int(quantity)

            cart_item.save()
            return Response({"message": "Product added to cart successfully."}, status=201)
        except Exception as e:
            return Response({"error": f"Failed to add product to cart: {str(e)}"}, status=400)

    def put(self, request):
        """
        Update the quantity of a product in the cart.
        """
        try:
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity')

            if not quantity or int(quantity) <= 0:
                return Response({"error": "Quantity must be greater than zero."}, status=400)

            cart = get_object_or_404(Cart, user=request.user)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

            cart_item.quantity = int(quantity)
            cart_item.save()
            return Response({"message": "Cart item quantity updated successfully."}, status=200)
        except Exception as e:
            return Response({"error": f"Failed to update cart item: {str(e)}"}, status=400)

    def delete(self, request):
        """
        Remove a product from the cart.
        """
        try:
            product_id = request.data.get('product_id')

            cart = get_object_or_404(Cart, user=request.user)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            cart_item.delete()

            return Response({"message": "Product removed from cart successfully."}, status=200)
        except Exception as e:
            return Response({"error": f"Failed to remove product from cart: {str(e)}"}, status=400)
