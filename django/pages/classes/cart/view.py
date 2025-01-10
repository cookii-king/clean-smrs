from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404
from ...models import Product, Cart, CartItem
from ...views import authenticate_user, check_mfa
class CartView(APIView):
    def post(self, request, product_id):
        try:
            if not request.user.is_authenticated:
                return redirect('login')
            account = request.user
            product = get_object_or_404(Product, id=product_id)
            cart, created = Cart.objects.get_or_create(customer=account)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not item_created:
                cart_item.quantity += 1
                cart_item.save()
            return redirect('cart')
        except Exception as e:
            message = f"'POST' Method Failed for CartView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def get(self, request):
        try:
            account = authenticate_user(request)
            check_mfa(account=account)
            cart = get_object_or_404(Cart, customer=account)
            cart_items = CartItem.objects.filter(cart=cart)
            context = {"cart_items": cart_items}
            return render(request, 'cart/cart.html', context)
        except Cart.DoesNotExist:
            return render(request, 'cart/cart.html', {"cart_items": []})
        except Exception as e:
            message = f"'GET' Method Failed for CartView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        
    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for CartView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def patch(self, request, cart_item_id):
        try:
            if not request.user.is_authenticated:
                return redirect('login')
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            quantity = int(request.data.get('quantity', 1))
            if quantity < 1:
                message = "Quantity must be at least 1."
                is_error = True
                status_code = 400
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
            cart_item.update_quantity(quantity)
            cart_total = sum(item.quantity * item.product.prices.first().unit_amount for item in cart_item.cart.cart_items.all())
            return Response({'item_id': str(cart_item.id), 'cart_total': cart_total}, status=200)
        except ValueError as e:
            message = f"Invalid quantity: {e}"
            is_error = True
            status_code = 400
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for CartView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request, cart_item_id):
        try:
            if not request.user.is_authenticated:
                return redirect('login')
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            cart_item.delete()
            cart_total = sum(item.quantity * item.product.prices.first().unit_amount for item in cart_item.cart.cart_items.all())
            return Response({'item_id': str(cart_item_id), 'cart_total': cart_total}, status=200)
        except Exception as e:
            message = f"'DELETE' Method Failed for CartView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for CartView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for CartView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')