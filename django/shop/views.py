from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrderSerializer, ProductSerializer, CartSerializer, SubscriptionSerializer
from .models import Order, Product, Cart, Subscription
from rest_framework.permissions import IsAuthenticated
from accounts.views import JWTAuthentication
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render, redirect
from .models import Subscription 
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartProduct
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

class OrderView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."})

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

class OrdersView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

@login_required    
def product_list(request):
    # Fetch all available products
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


def product_detail(request, product_id):
    # Fetch the product based on its ID
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


# Add product to the cart
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(account_id=request.user)
    
    # Check if the product is already in the cart, if so, increase the quantity
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_product.quantity += 1
        cart_product.save()

    return redirect('cart_view')

# Remove product from the cart
@login_required
def remove_from_cart(request, cart_product_id):
    cart_product = CartProduct.objects.get(id=cart_product_id)
    cart_product.delete()
    return redirect('cart_view')

# View cart
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(account_id=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def subscribe(request):
    if request.method == 'POST':
        # Logic for creating the subscription would go here.
        # For simplicity, we're just redirecting to the subscriptions page after subscribing.
        # You can add real subscription logic here.

        subscription_type = request.POST.get('subscription_type')

        # Example: create a new subscription for the user
        new_subscription = Subscription.objects.create(
            account=request.user, 
            subscription_type=subscription_type, 
            status='active'
        )
        
        # After subscribing, redirect the user to the subscription page
        return redirect('subscriptions')

    # If it's a GET request, just render the subscription form (optional)
    return render(request, 'subscription_form.html')

@login_required    
def subscription_view(request):
    return render(request, 'subscription.html') 

@login_required
def subscription_page(request):
    # Try to get the active subscription for the logged-in user
    try:
        subscription = Subscription.objects.get(account_id=request.user, status='active')
    except Subscription.DoesNotExist:
        subscription = None  # No active subscription for the user
    
    # Render the subscriptions page with the subscription data
    return render(request, 'subscription.html', {'subscription': subscription})





@login_required
class CartView(APIView):
    def get(self, request):
        # Assuming cart is fetched based on user (adjust logic based on your requirements)
        cart = Cart.objects.filter(user=request.user).first()
        return render(request, 'cart.html', {'cart': cart})


class OrderHistoryView(APIView):
    def get(self, request):
        # Fetch all orders for the logged-in user
        orders = Order.objects.filter(account_id=request.user)
        return render(request, 'order_history.html', {'orders': orders})

@login_required
class SubscriptionView(APIView):
    def get(self, request):
        # Assuming subscription is fetched based on user (adjust logic as needed)
        subscription = Subscription.objects.filter(user=request.user).first()
        return render(request, 'subscription.html', {'subscription': subscription})

def index(request):
    return render(request, 'index.html')
@login_required
def cart_page(request):
    return render(request, 'cart.html')