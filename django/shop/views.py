from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrderSerializer, ProductSerializer, CartSerializer, SubscriptionSerializer
from .models import Order, Product, Cart, Subscription
from rest_framework.permissions import IsAuthenticated
from accounts.views import JWTAuthentication
from django.shortcuts import render

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
    

class ProductView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."})
        
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

class ProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True) 
        return Response(serializer.data)

class CartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            account = request.user
            print(f"Account: {account.id}")
            cart = Cart.objects.get(account_id=account.id)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."})
        
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class SubscriptionView(APIView):
    def get(self, request, subscription_id):
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found."})
        
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

class SubscriptionsView(APIView):
    def get(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True) 
        return Response(serializer.data)
    
class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()  # Fetch all products from the database
        return render(request, 'products.html', {'products': products})


class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)  # Fetch the product by ID
        return render(request, 'product_detail.html', {'product': product})


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


class SubscriptionView(APIView):
    def get(self, request):
        # Assuming subscription is fetched based on user (adjust logic as needed)
        subscription = Subscription.objects.filter(user=request.user).first()
        return render(request, 'subscription.html', {'subscription': subscription})

def index(request):
    return render(request, 'index.html')

def cart_page(request):
    return render(request, 'cart.html')