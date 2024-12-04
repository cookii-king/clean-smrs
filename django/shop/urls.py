from django.urls import path
from .views import OrderView, OrdersView, ProductView, ProductsView, CartView, SubscriptionView, SubscriptionsView

urlpatterns = [
    path('order/create', OrderView.as_view(), name='order-create'),
    path('order/<uuid:order_id>', OrderView.as_view(), name='order-detail'),
    path('orders', OrdersView.as_view()),

    path('product/create', ProductView.as_view(), name='product-create'),
    path('product/<uuid:product_id>', ProductView.as_view(), name='product-detail'),
    path('products', ProductsView.as_view()),

    path('subscription/create', SubscriptionView.as_view(), name='subscription-create'),
    path('subscription/<uuid:subscription_id>', SubscriptionView.as_view(), name='subscription-detail'),
    path('subscriptions', SubscriptionsView.as_view()),

    path('cart', CartView.as_view(), name='cart-detail'),
]