from django.urls import path
from .views import PaymentLinksView

urlpatterns = [
    path('payment_links', PaymentLinksView.as_view()),    
]