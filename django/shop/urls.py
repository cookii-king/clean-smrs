from django.urls import path
from .views import OrderView, OrdersView, ProductView, CartView, SubscriptionView
urlpatterns = [
    path('order/create', OrderView.as_view(), name='order-create'),
    path('order/<uuid:order_id>/', OrderView.as_view(), name='order-detail'),
    path('orders', OrdersView.as_view()),

     # Product URLs
    path('product/create', ProductView.as_view(), name='product-create'),
    path('product/<uuid:product_id>/', ProductView.as_view(), name='product-detail'),

    # Cart URLs
    path('cart/create', CartView.as_view(), name='cart-create'),
    path('cart/<uuid:cart_id>/', CartView.as_view(), name='cart-detail'),

    # Subscription URLs
    path('subscription/create', SubscriptionView.as_view(), name='subscription-create'),
    path('subscription/<uuid:subscription_id>/', SubscriptionView.as_view(), name='subscription-detail'),
    
]