import io, pyotp, base64, qrcode
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib import messages
from ...models import ApiKey, Account, Subscription
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..authentication.view import JWTAuthentication, IsAuthenticated, LoginRequiredMixin, AuthenticationFailed

class AccountView(LoginRequiredMixin, APIView):
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
    
    def post(self, request):
 
        try:
            # Use the authenticate_user method
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            
            
            if not account.mfa_confirmed:
              return redirect("verify-mfa")
            if request.path == '/account/edit':
                name = request.POST.get('name')
                email = request.POST.get('email')
                description = request.POST.get('description')
                current_password = request.POST.get('current_password', '').strip()
                new_password = request.POST.get('new_password', '').strip()
                confirm_password = request.POST.get('confirm_password', '').strip()

                account.name = name
                account.email = email
                account.description = description

                if new_password:  # If new password is provided
                    if not current_password:
                        messages.error(request, "Please enter your current password to change your password.")
                        return render(request, 'account/edit.html', {'account': account})

                    if not check_password(current_password, account.password):
                        messages.error(request, "Current password is incorrect.")
                        return render(request, 'account/edit.html', {'account': account})

                    if new_password != confirm_password:
                        messages.error(request, "New passwords do not match.")
                        return render(request, 'account/edit.html', {'account': account})

                    account.set_password(new_password)

                try:
                    account.save()
                    messages.success(request, "Account details updated successfully.")
                    return redirect('account')  # Redirect to the account page
                except Exception as e:
                    messages.error(request, f"Failed to update account details: {str(e)}")
                    raise

            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for AccountView: {e}", "is_error": True}, status=400)
    
    # @method_decorator(login_required)
    def get(self, request):
        try:
            # Use the authenticate_user method
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            token = request.COOKIES.get('jwt')
            if request.path == '/account/edit':
                return render(request, 'account/edit.html',{"account": account, })
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            otp_uri = pyotp.totp.TOTP(account.mfa_secret).provisioning_uri(
                name=account.email,
                issuer_name="Clean SMRs"
            )

            qr = qrcode.make(otp_uri)
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")

            buffer.seek(0)
            qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")

            qr_code_data_uri = f"data:image/png;base64,{qr_code}"
            # Handle GET requests
            api_keys = ApiKey.objects.filter().all()
            
            print(f"stripe id: ${account.stripe_customer_id}")
            subscriptions = Subscription.objects.filter(
                   customer=account.stripe_customer_id, deleted__isnull=True, status='active' 
                ).all()
            print(f"subscriptions: ${subscriptions}")
            # Get the active subscription plan
            current_subscription = subscriptions.first() if subscriptions.exists() else None
            current_plan = None

            if current_subscription:
                # Assuming each subscription has one active subscription item
                subscription_item = current_subscription.subscription_items.first()
                if subscription_item:
                    current_plan = {
                        "name": subscription_item.price.product.name,
                        "amount": subscription_item.price.unit_amount,
                        "interval": subscription_item.price.recurring.get("interval", "N/A"),
                    }
            return render(request, 'account/account.html', {"api_keys": api_keys, "account": account,   'current_plan': current_plan, 'current_subscription': current_subscription, 'token': token, 'qrcode': qr_code_data_uri})
        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for AccountView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for AccountView: {e}", "is_error": True}, status=400)
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
            return Response(data={"error": f"'PUT' Method Failed for AccountView: {e}", "is_error": True}, status=400)
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
            return Response(data={"error": f"'PATCH' Method Failed for AccountView: {e}", "is_error": True}, status=400)
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
            return Response(data={"error": f"'DELETE' Method Failed for AccountView: {e}", "is_error": True}, status=400)
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
            return Response(data={"error": f"'OPTIONS' Method Failed for AccountView: {e}", "is_error": True}, status=400)
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
            return Response(data={"error": f"'HEAD' Method Failed for AccountView: {e}", "is_error": True}, status=400)