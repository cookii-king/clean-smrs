from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from ...models import Cart, CartItem, Product

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..authentication.view import JWTAuthentication, IsAuthenticated, LoginRequiredMixin, AuthenticationFailed

class CartView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    def check_mfa(self, account):
        if not account.mfa_confirmed and account.mfa_enabled:
              return redirect("verify-mfa")
    
    # @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            path = request.path

            if path == '/add-to-cart':
                return self.add_to_cart(request)

            if 'cart_item_id' in kwargs:
                cart_item_id = kwargs['cart_item_id']

                if path.startswith('/update-item/'):
                    return self.update_cart_item(request, cart_item_id)

                if path.startswith('/remove-item/'):
                    return self.remove_cart_item(request, cart_item_id)

            return Response({"error": "Invalid action."}, status=400)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response({"error": f"'POST' Method Failed for CartView: {e}"}, status=400)
    # @method_decorator(login_required)
    def add_to_cart(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)

        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity},
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return Response({"message": f"{product.name} added to cart successfully."}, status=201)
    # @method_decorator(login_required)
    def update_cart_item(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        quantity = request.data.get('quantity', 1)

        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            cart_item.delete()

        cart_total = sum(
            item.quantity * item.product.prices.first().unit_amount
            for item in cart_item.cart.cart_items.all()
            if item.product.prices.exists()
        )

        return Response({"message": "Cart item updated successfully.", "cart_total": cart_total}, status=200)
    # @method_decorator(login_required)
    def remove_cart_item(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()

        cart_total = sum(
            item.quantity * item.product.prices.first().unit_amount
            for item in cart_item.cart.cart_items.all()
            if item.product.prices.exists()
        )

        return Response({"message": "Cart item removed successfully.", "cart_total": cart_total, "item_id": cart_item_id}, status=200)
    # @method_decorator(login_required)
    def get(self, request):
        try:
            # Handle GET requests
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            cart, _ = Cart.objects.get_or_create(user=account)
            cart_items = cart.cart_items.all()  # Get all items in the cart
            # cart_items = CartItem.objects.filter(
            #     cart__user=request.user, 
            #     product__prices__isnull=False  # Exclude products without prices
            # ).distinct()

            # Calculate the total cost
            total = sum(
                item.quantity * item.product.prices.first().unit_amount for item in cart_items if item.product.prices.exists()
            )
            print(account.stripe_customer_id)
            print(cart)
            print(cart_items)
            return render(request, 'cart/cart.html', {"cart": cart, "cart_items": cart_items, 'total': total})
        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for CartView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for CartView: {e}"}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for CartView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for CartView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for CartView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for CartView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for CartView: {e}"}, status=400)