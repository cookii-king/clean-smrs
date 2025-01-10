import jwt, pyotp, datetime
from ...models import Account
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

def authenticate_user(request):
    """Authenticate the user using JWT and return the account."""
    jwt_auth = JWTAuthentication()
    account, _ = jwt_auth.authenticate(request)
    if account is None:
        raise AuthenticationFailed('Authentication failed')
    return account

def check_mfa(account):
    if not account.mfa_confirmed and account.mfa_enabled:
            return redirect("verify-mfa")

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

class ConfirmEmailView(APIView):
    def post(self, request):
        try:
            # Get the authenticated user's account
            account = request.user

            # Check if the request is to resend the confirmation code
            if request.data.get('resend') == 'true':
                # Generate a new confirmation secret and send email
                account.generate_email_confirmation_secret()
                account.send_confirmation_email()

                message = "Confirmation code resent successfully."
                is_error = False
                status_code = 200
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Handle email confirmation
            confirmation_code = request.data.get('confirmation_secret')

            # Validate input
            if not confirmation_code:
                message = "Confirmation code is required."
                is_error = True
                status_code = 400
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Validate confirmation code
            if account.email_confirmation_secret != confirmation_code:
                message = "Invalid confirmation code."
                is_error = True
                status_code = 401
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Mark email as confirmed
            account.validate_email_confirmed()

            # Success response
            message = "Email confirmed successfully."
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

        except Exception as e:
            # General exception handling
            message = f"'POST' Method Failed for ConfirmEmailView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def get(self, request):
        try:
            account = authenticate_user(request)
            check_mfa(account=account)
            # Handle GET requests
            # message = "GET request received"
            # is_error = False
            # status_code = 200
            # return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
            return render(request, 'authentication/confirm-email.html')
        except Exception as e:
            message = f"'GET' Method Failed for ConfirmEmailView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for ConfirmEmailView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def patch(self, request):
        try:
            # Handle PATCH requests
            message = "PATCH request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for ConfirmEmailView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request):
        try:
            # Handle DELETE requests
            message = "DELETE request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'DELETE' Method Failed for ConfirmEmailView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for ConfirmEmailView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for ConfirmEmailView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')


class VerifyMfaView(APIView):
    def post(self, request):
        try:
            # Extract account ID and OTP from the request data
            account_id = request.data.get("account_id")
            otp = request.data.get("otp")

            if not account_id or not otp:
                message = "Account ID and OTP are required."
                is_error = True
                status_code = 400
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Retrieve the account using the account_id
            account = Account.objects.get(id=account_id)

            # Verify the OTP using the account's MFA secret
            totp = pyotp.TOTP(account.mfa_secret)
            if totp.verify(otp):
                # If OTP is correct, mark MFA as confirmed
                account.validate_mfa_confirmed()
                message = "MFA verification successful."
                is_error = False
                status_code = 200
            else:
                # If OTP is incorrect, return an error
                message = "Invalid OTP. Please try again."
                is_error = True
                status_code = 400

        except Account.DoesNotExist:
            message = "Account not found."
            is_error = True
            status_code = 404
        except Exception as e:
            message = f"'POST' Method Failed for VerifyMfaView: {e}"
            is_error = True
            status_code = 500

        return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    
    def get(self, request):
        try:
            account = authenticate_user(request)
            check_mfa(account=account)
            # Handle GET requests
            # message = "GET request received"
            # is_error = False
            # status_code = 200
            # return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
            return render(request, 'authentication/verify-mfa.html', {"account_id": account.id})
        except Exception as e:
            message = f"'GET' Method Failed for VerifyMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for VerifyMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def patch(self, request):
        try:
            # Handle PATCH requests
            message = "PATCH request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for VerifyMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request):
        try:
            # Handle DELETE requests
            message = "DELETE request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'DELETE' Method Failed for VerifyMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for VerifyMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for VerifyMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')


class EnableMfaView(APIView):
    def post(self, request):
        try:
            # Get the authenticated user's account
            account = request.user

            # Generate a new MFA secret if it doesn't exist
            if not account.mfa_secret:
                account.generate_mfa_secret_secret()

            # Get the MFA code from the request
            mfa_code = request.data.get('otp')

            # Validate input
            if not mfa_code:
                message = "MFA code is required."
                is_error = True
                status_code = 400
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Verify the MFA code
            totp = pyotp.TOTP(account.mfa_secret)
            if not totp.verify(mfa_code):
                message = "Invalid MFA code."
                is_error = True
                status_code = 401
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Enable MFA for the account
            account.mfa_enabled = True
            account.save()

            # Success response
            message = "MFA enabled successfully."
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

        except Exception as e:
            # General exception handling
            message = f"'POST' Method Failed for EnableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def get(self, request):
        try:
            account = authenticate_user(request)
            check_mfa(account=account)
            # Handle GET requests
            # message = "GET request received"
            # is_error = False
            # status_code = 200
            # return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
            return render(request, 'authentication/enable-mfa.html', {'account':account})
        except Exception as e:
            message = f"'GET' Method Failed for EnableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for EnableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def patch(self, request):
        try:
            # Handle PATCH requests
            message = "PATCH request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for EnableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request):
        try:
            # Handle DELETE requests
            message = "DELETE request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'DELETE' Method Failed for EnableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for EnableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for EnableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

class DisableMfaView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            message = "POST request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'POST' Method Failed for DisableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def get(self, request):
        try:
            account = authenticate_user(request)
            check_mfa(account=account)
            # Handle GET requests
            message = "GET request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'GET' Method Failed for DisableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for DisableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def patch(self, request):
        try:
            # Handle PATCH requests
            message = "PATCH request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for DisableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request):
        try:
            # Handle DELETE requests
            message = "DELETE request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'DELETE' Method Failed for DisableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for DisableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for DisableMfaView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')


class LoginView(APIView):
    def post(self, request):
        try:
            # Extract email and password from request
            email = request.data.get('email')
            password = request.data.get('password')

            # Validate input
            if not email or not password:
                message = "Email and password are required."
                is_error = True
                status_code = 400
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Check if account exists
            account = Account.objects.filter(email=email).first()
            if not account:
                message = "Account not found."
                is_error = True
                status_code = 404
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Authenticate user
            user = authenticate(request, username=account.username, password=password)
            if not user:
                message = "Invalid credentials."
                is_error = True
                status_code = 401
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Log the user in
            login(request, user)

            # Create JWT token
            try:
                payload = {
                    'id': str(account.id),
                    'username': str(account.username),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                token = jwt.encode(payload, 'secret-key', algorithm='HS256')
            except Exception as e:
                message = f"Failed to create JWT: {e}"
                is_error = True
                status_code = 500
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Set token in response cookie
            response = redirect('index')  # Redirect to homepage (index.html)
            response.set_cookie(key='jwt', value=token, httponly=True)

            return response

        except Exception as e:
            # General exception handling
            message = f"'POST' Method Failed for LoginView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def get(self, request):
        try:
            # Handle GET requests
            # message = "GET request received"
            # is_error = False
            # status_code = 200
            # return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
            return render(request, 'authentication/login.html')
        except Exception as e:
            message = f"'GET' Method Failed for LoginView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for LoginView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def patch(self, request):
        try:
            # Handle PATCH requests
            message = "PATCH request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for LoginView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request):
        try:
            # Handle DELETE requests
            message = "DELETE request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'DELETE' Method Failed for LoginView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for LoginView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for LoginView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')


class RegisterView(APIView):
    def post(self, request):
        try:
            # Extract data from request
            email = request.data.get('email')
            password = request.data.get('password')
            username = request.data.get('username')
            name = request.data.get('name')

            # Validate input
            if not email or not password or not username:
                message = "Email, password, and username are required."
                is_error = True
                status_code = 400
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Check if email or username already exists
            if Account.objects.filter(email=email).exists():
                message = "Email is already in use."
                is_error = True
                status_code = 409
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            if Account.objects.filter(username=username).exists():
                message = "Username is already in use."
                is_error = True
                status_code = 409
                return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

            # Create new account
            account = Account(
                email=email,
                name=name,
                username=username,
                password=make_password(password)  # Hash the password
            )
            account.save()
            account.create_stripe_customer()

            # Success response
            message = "Account created successfully."
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

        except Exception as e:
            # General exception handling
            message = f"'POST' Method Failed for RegisterView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def get(self, request):
        try:
            # Handle GET requests
            # message = "GET request received"
            # is_error = False
            # status_code = 200
            # return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
            return render(request, 'authentication/register.html')
        except Exception as e:
            message = f"'GET' Method Failed for RegisterView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for RegisterView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def patch(self, request):
        try:
            # Handle PATCH requests
            message = "PATCH request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for RegisterView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request):
        try:
            # Handle DELETE requests
            message = "DELETE request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'DELETE' Method Failed for RegisterView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for RegisterView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for RegisterView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    

class LogoutView(APIView):
    def post(self, request):
        try:
            # Log out the user
            logout(request)

            # Clear the JWT token from cookies
            response = redirect('index')  # Redirect to homepage (index.html)
            response.delete_cookie('jwt')

            # Success response
            message = "Successfully logged out."
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

        except Exception as e:
            # General exception handling
            message = f"'POST' Method Failed for LogoutView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def get(self, request):
        try:
            account = authenticate_user(request)
            check_mfa(account=account)
            # Handle GET requests
            message = "GET request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'GET' Method Failed for LogoutView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for LogoutView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def patch(self, request):
        try:
            # Handle PATCH requests
            message = "PATCH request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PATCH' Method Failed for LogoutView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def delete(self, request):
        try:
            # Handle DELETE requests
            message = "DELETE request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'DELETE' Method Failed for LogoutView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            message = "OPTIONS request received"
            is_error = False
            status_code = 204
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'OPTIONS' Method Failed for LogoutView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            message = "HEAD request received"
            is_error = False
            status_code = 200
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'HEAD' Method Failed for LogoutView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')