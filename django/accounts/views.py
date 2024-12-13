from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .serializers import AccountSerializer
from .models import Account
import datetime
import jwt
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
from django.contrib.auth import login
from accounts.models import Account 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMessage
from cleansmrs_system.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD



# JWT Authentication
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header:
            try:
                token_type, token = auth_header.split()
                if token_type.lower() != 'bearer':
                    raise AuthenticationFailed('Invalid token type')
            except ValueError:
                raise AuthenticationFailed('Invalid token header')
        else:
            token = request.COOKIES.get('jwt')

        if not token:
            return None
        try:
            payload = jwt.decode(token, 'secret-key', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        account = Account.objects.filter(id=payload['id']).first()
        if account is None:
            raise AuthenticationFailed('User not found')

        return (account, None)
    
class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add username to context if the user is authenticated
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        
        return context
    
       
class AccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = request.user
        token = request.COOKIES.get('jwt')
        return render(request, 'account.html', {
            'name': account.name,
            'email': account.email,
            'token': token,
            'email_confirmed': account.email_confirmed
             })
class ConfirmEmailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        account = request.user
        if(account.email_confirmation_secret == request.data["confirmation_secret"]):
            account.validate_email_confirmed()
            return redirect('account')
        else:
            return Response(data={"error":"email could not be confirmed"})

    # def get(self, request):
    #     account = request.user
    #     if(account.email_confirmation_secret == None):
    #         account.generate_email_confirmation_secret()
    #         send_mail(subject=f"Please confirm your email ${account.name??account.username}", message=f"You confirmation secret is: ${account.email_confirmation_secret}", from_email=DEFAULT_FROM_EMAIL, auth_user=EMAIL_HOST_USER, auth_password=EMAIL_HOST_PASSWORD, recipient_list=["cookiekingsn2001@gmail.com"], fail_silently=True)
    #     else:
    #         pass
    #     return render(request, 'confirm_email.html')
    def get(self, request):
        account = request.user

        if not account.email_confirmation_secret:
            # Generate a new email confirmation secret
            account.generate_email_confirmation_secret()

            # Determine the name to use in the email subject
            if account.name:
                user_name = account.name
            elif account.username:
                user_name = account.username
            else:
                user_name = "Please confirm your email"  # Default message

            # Send confirmation email
            try:
                send_mail(
                    subject=f"Please confirm your email, {user_name}" if user_name != "Please confirm your email" else user_name,
                    message=f"Your confirmation secret is: {account.email_confirmation_secret}",
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[account.email],  # Send to user's email
                    fail_silently=False,  # Set to False to raise exceptions on failure
                )
            except Exception as e:
                # Log or handle the email sending error as needed
                print(f"Failed to send email: {e}")
        else:
            # Secret already exists; optionally handle this case
            pass

        # Render the confirmation email page
        return render(request, 'confirm_email.html')

class RegisterView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        # Generate a JWT token for the registered user
        payload = {
            'id': str(account.id),  # Convert UUID to string
            'username': str(account.username),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret-key', algorithm='HS256')
        
        response = redirect('confirm-email')  # Redirects to /account
        response.set_cookie(key='jwt', value=token, httponly=True)  # Set the JWT token in the cookies
        
        # return Response(serializer.data)
        return response
    
    def get(self, request):
        return render(request, 'register.html')
    
class LoginView(APIView):
    def get(self, request):
        # Render the login page
        return render(request, 'login.html')

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Attempt to find the user
        account = Account.objects.filter(email=email).first()

        if account is None:
            raise AuthenticationFailed('Account not found!')

        # Check if the password matches
        if not account.check_password(password):
            raise AuthenticationFailed('Incorrect email or password!')

        # Log the user in
        login(request, account)

        # Generate JWT token (optional, if you are using tokens)
        payload = {
            'id': str(account.id),
            'username': str(account.username),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret-key', algorithm='HS256')

        # Set JWT token in cookies
        response = redirect('/')  # Redirect to homepage (index.html)
        response.set_cookie(key='jwt', value=token, httponly=True)

        return response
    

class LogoutView(View):
    def post(self, request):
        logout(request)
        # return redirect('login')
        response = redirect('/')  # Redirects to the homepage (/)
        response.delete_cookie('jwt')  # Delete the JWT token cookie
        return response
    
    def get(self, request):
        logout(request)
        # return redirect('login')
        response = redirect('/')  # Redirects to the homepage (/)
        response.delete_cookie('jwt')  # Delete the JWT token cookie
        return response
    



@login_required
def home(request):
    # Access the logged-in user's username
    username = request.user.username
    return render(request, 'home.html', {'username': username})
    