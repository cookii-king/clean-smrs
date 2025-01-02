# django/pages/classes/cart/view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from pages.classes.cart.model import Cart, CartItem
from pages.classes.product.model import Product
from pages.classes.cart.serializer import CartSerializer
from django.views import View
from django.http import JsonResponse


class CartView(View):
    """
    Render the shopping cart page.
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required."}, status=403)

        # Fetch the user's cart
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)  # Ensure proper queryset
        total_price = sum(item.quantity * item.product.price for item in cart_items)

        context = {
            'cart': {
                'items': cart_items,  # Pass queryset, not the manager
                'total_price': total_price
            }
        }
        return render(request, 'cart.html', context)



class CartAPIView(APIView):
    """
    API endpoints for managing cart actions.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the user's cart and its items as JSON.
        """
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        Add a product to the cart or update its quantity if it already exists.
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Check if the cart already has this product
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += int(quantity)  # Update the quantity
        else:
            cart_item.quantity = int(quantity)  # Set the quantity

        cart_item.save()
        return Response({"message": "Product added to cart successfully."}, status=201)

    def put(self, request):
        """
        Update the quantity of a product in the cart.
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not quantity or int(quantity) <= 0:
            return Response({"error": "Quantity must be greater than zero."}, status=400)

        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        cart_item.quantity = int(quantity)
        cart_item.save()

        return Response({"message": "Cart item quantity updated successfully."}, status=200)

    def delete(self, request):
        """
        Remove a product from the cart.
        """
        product_id = request.data.get('product_id')

        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()

        return Response({"message": "Product removed from cart successfully."}, status=200)

    def clear(self, request):
        """
        Clear all items from the cart.
        """
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response({"message": "Cart cleared successfully."}, status=200)
