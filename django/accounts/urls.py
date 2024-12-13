from django.urls import path
from .views import AccountView, ConfirmEmailView, RegisterView, LoginView,  LogoutView, HomePageView
from django.contrib.auth import views as auth_views
from .views import HomePageView 



urlpatterns = [
    path('account', AccountView.as_view(), name='account'),
    path('confirm-email', ConfirmEmailView.as_view(), name='confirm-email'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('', HomePageView.as_view(), name='home'),  # Correct usage of HomePageView as a class-based view
]
