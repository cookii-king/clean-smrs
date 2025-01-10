import uuid, pyotp, random, qrcode, io, base64
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from ...models import ApiKey, Subscription
from ...views import authenticate_user, check_mfa
from django.contrib import messages 

class AccountView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            # message = "POST request received"
            # is_error = False
            # status_code = 201
            # return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
            # Use the authenticate_user method
            account = authenticate_user(request)
            check_mfa(account=account)
            
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
                    messages.er
        except Exception as e:
            message = f"'POST' Method Failed for AccountView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def get(self, request):
        try:
            # Get the authenticated user's account
            account = authenticate_user(request)
            check_mfa(account=account)
            if(account.mfa_secret == None):
                account.generate_mfa_secret_secret()
            
            if request.path == '/account/edit':
                return render(request, 'account/edit.html',{"account": account, })

            # Generate MFA QR code if needed
            # qr_code_data_uri = None
            # if not account.mfa_enabled and account.mfa_secret is None:
            #     account.generate_mfa_secret_secret()
            #     otp_uri = pyotp.totp.TOTP(account.mfa_secret).provisioning_uri(
            #         name=account.email,
            #         issuer_name="Clean SMRs"
            #     )
            #     qr = qrcode.make(otp_uri)
            #     buffer = io.BytesIO()
            #     qr.save(buffer, format="PNG")
            #     buffer.seek(0)
            #     qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")
            #     qr_code_data_uri = f"data:image/png;base64,{qr_code}"
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

            # Fetch API keys and subscriptions
            api_keys = ApiKey.objects.filter(account=account)
            subscriptions = Subscription.objects.filter(
                customer=account.stripe_customer_id, deleted__isnull=True, status='active'
            )

            # Get the active subscription plan
            current_subscription = subscriptions.first() if subscriptions.exists() else None
            current_plan = None
            if current_subscription:
                subscription_item = current_subscription.subscription_items.first()
                if subscription_item:
                    current_plan = {
                        "name": subscription_item.price.product.name,
                        "amount": subscription_item.price.unit_amount,
                        "interval": subscription_item.price.recurring.get("interval", "N/A"),
                    }

            # Render the account page with user data
            return render(request, 'account/account.html', {
                'account': account,
                'api_keys': api_keys,
                'current_plan': current_plan,
                'current_subscription': current_subscription,
                'token': request.COOKIES.get('jwt'),
                'qrcode': qr_code_data_uri,
            })
        except Exception as e:
            message = f"'GET' Method Failed for AccountView: {e}"
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
            message = f"'PUT' Method Failed for AccountView: {e}"
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
            message = f"'PATCH' Method Failed for AccountView: {e}"
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
            message = f"'DELETE' Method Failed for AccountView: {e}"
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
            message = f"'OPTIONS' Method Failed for AccountView: {e}"
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
            message = f"'HEAD' Method Failed for AccountView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')