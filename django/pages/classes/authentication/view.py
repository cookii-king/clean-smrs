import jwt
from ...models import Account
from ...serializers import AccountSerializer
import datetime
import pyotp
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from system.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

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

class ConfirmEmailView(LoginRequiredMixin, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            account = request.user
            if(account.email_confirmation_secret == request.data["confirmation_secret"]):
                account.validate_email_confirmed()
                return redirect('account')
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for ConfirmEmailView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            if(account.email_confirmation_secret == None):
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
                    email_exception = f"Failed to send email: {e}"
                    raise Exception(email_exception)
            return render(request, 'confirm-email.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for ConfirmEmailView: {e}"}, status=400)

class VerifyMfaView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            account_id = request.data["account_id"]
            otp = request.data["otp"]
            print(f"request: {request.data}")
            if not account_id or not otp:
                return Response({"error": "Account ID and OTP are required."}, status=400)
            account = Account.objects.get(id=account_id)
            totp = pyotp.TOTP(account.mfa_secret)
            if(totp.verify(otp)):
                # account.validate_mfa_enabled()
                login(request, account)
                payload = {
                    'id': str(account.id),
                    'username': str(account.username),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                token = jwt.encode(payload, 'secret-key', algorithm='HS256')
                
                response = redirect('account')  # Redirect to homepage (index.html)
                response.set_cookie(key='jwt', value=token, httponly=True)
                return response
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for VerifyMfaView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            return render(request, 'verify-mfa.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for VerifyMfaView: {e}"}, status=400)
        
class VerifyMfaView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            account_id = request.data["account_id"]
            otp = request.data["otp"]
            print(f"request: {request.data}")
            if not account_id or not otp:
                return Response({"error": "Account ID and OTP are required."}, status=400)
            account = Account.objects.get(id=account_id)
            totp = pyotp.TOTP(account.mfa_secret)
            if(totp.verify(otp)):
                # account.validate_mfa_enabled()
                login(request, account)
                payload = {
                    'id': str(account.id),
                    'username': str(account.username),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                token = jwt.encode(payload, 'secret-key', algorithm='HS256')
                
                response = redirect('account')  # Redirect to homepage (index.html)
                response.set_cookie(key='jwt', value=token, httponly=True)
                return response
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for VerifyMfaView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            return render(request, 'verify-mfa.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for VerifyMfaView: {e}"}, status=400)

class EnableMfaView(LoginRequiredMixin, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            account = request.user
            otp = request.data["otp"]
            if not account:
                return render(request, 'enable-mfa.html', {'account': account})
            totp = pyotp.TOTP(account.mfa_secret)
            if(totp.verify(otp)):
                account.validate_mfa_enabled()
                return redirect('account')
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for EnableMfaView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            return render(request, 'enable-mfa.html', {'account':account})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for EnableMfaView: {e}"}, status=400)

class DisableMfaView(LoginRequiredMixin, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            account = request.user
            account.disable_mfa_enabled()
            return redirect('account')

        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for DisableMfaView: {e}"}, status=400)

class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            account = Account.objects.filter(email=email).first()
            
            if account is None:
                raise AuthenticationFailed('Account not found!')
            
            if not account.check_password(password):
                raise AuthenticationFailed('Incorrect email or password!')
            
            if account is not None:
                if account.mfa_enabled:
                    # Redirect to the verify MFA page
                    return render(request, 'verify-mfa.html', {'account_id': account.id})
                else:
                    login(request, account)
                    
                    payload = {
                        'id': str(account.id),
                        'username': str(account.username),
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                        'iat': datetime.datetime.utcnow()
                    }
                    token = jwt.encode(payload, 'secret-key', algorithm='HS256')
                    
                    response = redirect('index')  # Redirect to homepage (index.html)
                    response.set_cookie(key='jwt', value=token, httponly=True)
                    return response
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for LoginView: {e}"}, status=400)
    
    def get(self, request):
        try:
            return render(request, 'login.html')
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for LoginView: {e}"}, status=400)

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = AccountSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            account.create_in_stripe()
            
            login(request, account)
            
            payload = {
                'id': str(account.id),
                'username': str(account.username),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret-key', algorithm='HS256')
            
            response = redirect('index')  # Redirect to homepage (index.html)
            response.set_cookie(key='jwt', value=token, httponly=True)
            return response
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for RegisterView: {e}"}, status=400)
    
    def get(self, request):
        try:
            return render(request, 'register.html')
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for RegisterView: {e}"}, status=400)

class LogoutView(LoginRequiredMixin, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            logout(request)
            response = redirect('index')  # Redirect to homepage (index.html)
            response.delete_cookie('jwt')
            response.delete_cookie('csrftoken')
            return response
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for LogoutView: {e}"}, status=400)
    
    def get(self, request):
        try:
            logout(request)
            response = redirect('index')  # Redirect to homepage (index.html)
            response.delete_cookie('jwt')
            response.delete_cookie('csrftoken')
            return response
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for LogoutView: {e}"}, status=400)