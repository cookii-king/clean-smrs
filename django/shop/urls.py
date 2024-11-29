from django.urls import path
from .views import OrderView, OrdersView

urlpatterns = [
    path('order/create', OrderView.as_view(), name='order-create'),
    path('order/<uuid:order_id>/', OrderView.as_view(), name='order-detail'),
    path('orders', OrdersView.as_view()),
]