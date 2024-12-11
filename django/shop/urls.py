from django.urls import path
from .views import OrderView, OrdersView, CartView, index, cart_page
from . import views 


urlpatterns = [

    path('', index, name='home'),
    path('cart', cart_page, name='cart'),
    
    path('order/create', OrderView.as_view(), name='order-create'),
    path('order/<uuid:order_id>', OrderView.as_view(), name='order-detail'),
    path('orders', OrdersView.as_view()),

    path('products/', views.product_list, name='product_list'),  # Product list page
    path('product/<uuid:product_id>/', views.product_detail, name='product_detail'),  # Product detail page

    path('product/<uuid:product_id>/', views.product_detail, name='product_detail'),
    #path('add_to_cart/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    #path('buy_now/<uuid:product_id>/', views.buy_now, name='buy_now'),

    path('subscriptions/', views.subscription_page, name='subscriptions'),
    path('subscribe/', views.subscribe, name='subscribe'), 
    path('subscription/', views.subscription_view, name='subscription'),

    path('add_to_cart/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<uuid:cart_product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart', views.cart_view, name='cart_view'), 
]