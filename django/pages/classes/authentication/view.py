from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from ...models import Cart, CartItem, Product, Account
from ...serializers import AccountSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.core.mail import send_mail
import jwt, pyotp, datetime
from system.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    def check_mfa(self, account):
        if not account.mfa_confirmed and account.mfa_enabled:
              return redirect("verify-mfa")
    # @method_decorator(login_required)
    def post(self, request):
        try:
            # Use the authenticate_user method
            account = self.authenticate_user(request)
            self.check_mfa(account=account)

            if 'resend' in request.data:
                # Resend confirmation code
                account.generate_email_confirmation_secret()
                self.send_confirmation_email(account)
                return render(request, 'authentication/confirm-email.html', {"message": "Confirmation code resent."})

            if account.email_confirmation_secret == request.data["confirmation_secret"]:
                account.validate_email_confirmed()
                return redirect('account')
            else:
                return render(request, 'authentication/confirm-email.html', {"error": "Invalid confirmation code."})

        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for ConfirmEmailView: {e}"}, status=400)

    def get(self, request):
        try:
            # Use the authenticate_user method
            account = self.authenticate_user(request)
            self.check_mfa(account=account)

            if account.email_confirmation_secret is None:
                account.generate_email_confirmation_secret()
                self.send_confirmation_email(account)

            return render(request, 'authentication/confirm-email.html')
        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for ConfirmEmailView: {e}"}, status=400)

    def send_confirmation_email(self, account):
        """Send the confirmation email to the user."""
        user_name = account.name or account.username or "Please confirm your email"
        try:
            send_mail(
                subject=f"Please confirm your email, {user_name}" if user_name != "Please confirm your email" else user_name,
                message=f"Your confirmation secret is: {account.email_confirmation_secret}",
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[account.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise Exception(f"Failed to send email: {e}")
        # @method_decorator(login_required)
    # def get(self, request):
    #     try:
    #         # Use the authenticate_user method
    #         account = self.authenticate_user(request)
    #         self.check_mfa(account=account)
    #         if(account.email_confirmation_secret == None):
    #             account.generate_email_confirmation_secret()
    #             # Determine the name to use in the email subject
    #             if account.name:
    #                 user_name = account.name
    #             elif account.username:
    #                 user_name = account.username
    #             else:
    #                 user_name = "Please confirm your email"  # Default message

    #             # Send confirmation email
    #             try:
    #                 send_mail(
    #                     subject=f"Please confirm your email, {user_name}" if user_name != "Please confirm your email" else user_name,
    #                     message=f"Your confirmation secret is: {account.email_confirmation_secret}",
    #                     from_email=DEFAULT_FROM_EMAIL,
    #                     recipient_list=[account.email],  # Send to user's email
    #                     fail_silently=False,  # Set to False to raise exceptions on failure
    #                 )
    #             except Exception as e:
    #                 # Log or handle the email sending error as needed
    #                 print(f"Failed to send email: {e}")
    #                 email_exception = f"Failed to send email: {e}"
    #                 raise Exception(email_exception)
    #         # Handle GET requests
    #         return render(request, 'authentication/confirm-email.html')
    #     except AuthenticationFailed as e:
    #         return redirect('login')  
    #     except Exception as e:
    #                 return Response(data={"error": f"'GET' Method Failed for ConfirmEmailView: {e}"}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            # Use the authenticate_user method
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for ConfirmEmailView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            # Use the authenticate_user method
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for ConfirmEmailView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            # Use the authenticate_user method
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for ConfirmEmailView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            # Use the authenticate_user method
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for ConfirmEmailView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            # Use the authenticate_user method
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for ConfirmEmailView: {e}"}, status=400)

class VerifyMfaView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    def check_mfa(self, account):
        if not account.mfa_confirmed and account.mfa_enabled:
              return redirect("verify-mfa")
    # @method_decorator(login_required)
    def post(self, request):
        try:
            # account = self.authenticate_user(request)
            # self.check_mfa(account=account)
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
                account.validate_mfa_confirmed()
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
            else:
                response = redirect('verify-mfa')
                return response

            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for VerifyMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def get(self, request):
        try:
            account = request.user
            # account = self.authenticate_user(request)
            # self.check_mfa(account=account)
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            # Handle GET requests
            return render(request, 'authentication/verify-mfa.html', {"account_id": account.id})
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for VerifyMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            # account = self.authenticate_user(request)
            # self.check_mfa(account=account)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for VerifyMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            # account = self.authenticate_user(request)
            # self.check_mfa(account=account)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for VerifyMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            # account = self.authenticate_user(request)
            # self.check_mfa(account=account)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for VerifyMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            # account = self.authenticate_user(request)
            # self.check_mfa(account=account)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for VerifyMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            # account = self.authenticate_user(request)
            # self.check_mfa(account=account)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for VerifyMfaView: {e}"}, status=400)

class EnableMfaView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    def check_mfa(self, account):
        if not account.mfa_confirmed and account.mfa_enabled:
              return redirect("verify-mfa")
    # @method_decorator(login_required)
    def post(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            otp = request.data["otp"]
            if not account:
                return render(request, 'enable-mfa.html', {'account': account})
            totp = pyotp.TOTP(account.mfa_secret)
            if(totp.verify(otp)):
                account.validate_mfa_enabled()
                return redirect('account')
            else:
                response = redirect('enable-mfa')
                return response
            # Handle POST requests
            # return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for EnableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def get(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            # Handle GET requests
            return render(request, 'authentication/enable-mfa.html', {'account':account})
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for EnableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for EnableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for EnableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for EnableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for EnableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for EnableMfaView: {e}"}, status=400)

class DisableMfaView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    def check_mfa(self, account):
        if not account.mfa_confirmed and account.mfa_enabled:
              return redirect("verify-mfa")
    # @method_decorator(login_required)
    def post(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            account.disable_mfa_enabled()
            return redirect('account')
            return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for DisableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def get(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle GET requests
            return render(request, 'authentication/disable-mfa.html')
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for DisableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for DisableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for DisableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for DisableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for DisableMfaView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for DisableMfaView: {e}"}, status=400)

class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            account = Account.objects.filter(email=email).first()
            if account is None:
                raise 'Account not found!'
            if not account.check_password(password):
                raise 'Incorrect email or password!'
            if account is not None:
                if account.mfa_enabled:
                    login(request, account)
                    # Redirect to the verify MFA page
                    return redirect('verify-mfa')
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
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for LoginView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'authentication/login.html')
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for LoginView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for LoginView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for LoginView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for LoginView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for LoginView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for LoginView: {e}"}, status=400)

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = AccountSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            account.create_or_get_stripe_customer()
            
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
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for RegisterView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'authentication/register.html')
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for RegisterView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for RegisterView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for RegisterView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for RegisterView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for RegisterView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for RegisterView: {e}"}, status=400)

class LogoutView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    def check_mfa(self, account):
        if not account.mfa_confirmed and account.mfa_enabled:
              return redirect("verify-mfa")
    # @method_decorator(login_required)
    def post(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            account.validate_mfa_unconfirmed()
            logout(request)
            response = redirect('index')  # Redirect to homepage (index.html)
            response.delete_cookie('jwt')
            response.delete_cookie('csrftoken')
            return response
            # return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for LogoutView: {e}"}, status=400)
    # @method_decorator(login_required)
    def get(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            logout(request)
            # Handle GET requests
            # return render(request, 'authentication/logout.html')
            # return Response({"message": "GET request received"}, status=201)
            response = redirect('index')  # Redirect to homepage (index.html)
            response.delete_cookie('jwt')
            response.delete_cookie('csrftoken')
            return response
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for LogoutView: {e}"}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for LogoutView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for LogoutView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for LogoutView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for LogoutView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for LogoutView: {e}"}, status=400)
