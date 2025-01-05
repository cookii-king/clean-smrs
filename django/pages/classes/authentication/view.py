from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from ...models import Cart, CartItem, Product, Account
from ...serializers import AccountSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.core.mail import send_mail
import jwt, pyotp, datetime
from system.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


class ConfirmEmailView(APIView):
    def post(self, request):
        try:
            account = request.user
            if(account.email_confirmation_secret == request.data["confirmation_secret"]):
                account.validate_email_confirmed()
                return redirect('account')
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
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
            # Handle GET requests
            return render(request, 'authentication/confirm-email.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for ConfirmEmailView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for ConfirmEmailView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for ConfirmEmailView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for ConfirmEmailView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for ConfirmEmailView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for ConfirmEmailView: {e}"}, status=400)

class VerifyMfaView(APIView):
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
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for VerifyMfaView: {e}"}, status=400)

    def get(self, request):
        try:
            account = request.user
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            # Handle GET requests
            return render(request, 'authentication/verify-mfa.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for VerifyMfaView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for VerifyMfaView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for VerifyMfaView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for VerifyMfaView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for VerifyMfaView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for VerifyMfaView: {e}"}, status=400)

class EnableMfaView(APIView):
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
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for EnableMfaView: {e}"}, status=400)

    def get(self, request):
        try:
            account = request.user
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            # Handle GET requests
            return render(request, 'authentication/enable-mfa.html', {'account':account})
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for EnableMfaView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for EnableMfaView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for EnableMfaView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for EnableMfaView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for EnableMfaView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for EnableMfaView: {e}"}, status=400)

class DisableMfaView(APIView):
    def post(self, request):
        try:
            account = request.user
            account.disable_mfa_enabled()
            return redirect('account')
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for DisableMfaView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'authentication/disable-mfa.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for DisableMfaView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for DisableMfaView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for DisableMfaView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for DisableMfaView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for DisableMfaView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
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
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for LoginView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'authentication/login.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for LoginView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for LoginView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for LoginView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for LoginView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for LoginView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for LoginView: {e}"}, status=400)

class LogoutView(APIView):
    def post(self, request):
        try:
            logout(request)
            response = redirect('index')  # Redirect to homepage (index.html)
            response.delete_cookie('jwt')
            response.delete_cookie('csrftoken')
            return response
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for LogoutView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            # return render(request, 'authentication/logout.html')
            return Response({"message": "GET request received"}, status=201)
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for LogoutView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for LogoutView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for LogoutView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for LogoutView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for LogoutView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for LogoutView: {e}"}, status=400)

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
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for RegisterView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'authentication/register.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for RegisterView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for RegisterView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for RegisterView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for RegisterView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for RegisterView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for RegisterView: {e}"}, status=400)
