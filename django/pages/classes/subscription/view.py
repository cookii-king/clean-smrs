from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from ...models import Account, Subscription
from ...views import authenticate_user, check_mfa

class SubscriptionView(APIView):
    def post(self, request):
        try:
            # Authenticate the user
            account = authenticate_user(request)

            # Check if the request is to cancel a subscription
            if request.path == '/subscription/cancel':
                subscription_id = request.data.get('subscription_id')
                subscription = Subscription.objects.filter(id=subscription_id, customer=account).first()

                # Check if the subscription exists
                if not subscription:
                    message = "Subscription not found."
                    is_error = True
                    status_code = 404
                    return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

                # Cancel the subscription
                subscription.cancel_subscription()
                return redirect('subscriptions')

            # If the action is invalid
            message = "Invalid action."
            is_error = True
            status_code = 400
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

        except AuthenticationFailed as e:
            # Redirect to login if authentication fails
            return redirect('login')

        except Exception as e:
            # Handle any other exceptions
            message = f"Failed to cancel subscription: {e}"
            is_error = True
            status_code = 400
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
            return render(request, 'subscription/subscription.html')
        except Exception as e:
            message = f"'GET' Method Failed for SubscriptionView: {e}"
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
            message = f"'PUT' Method Failed for SubscriptionView: {e}"
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
            message = f"'PATCH' Method Failed for SubscriptionView: {e}"
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
            message = f"'DELETE' Method Failed for SubscriptionView: {e}"
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
            message = f"'OPTIONS' Method Failed for SubscriptionView: {e}"
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
            message = f"'HEAD' Method Failed for SubscriptionView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')


class SubscriptionsView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            message = "POST request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'POST' Method Failed for SubscriptionsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def get(self, request):
        try:
            # Authenticate the user
            account = authenticate_user(request)
            check_mfa(account=account)

            # Fetch all subscriptions (active and inactive) for the user
            subscriptions = Subscription.objects.filter(
                customer=account.stripe_customer_id
            ).select_related('customer').prefetch_related('subscription_items__price', 'subscription_items__plan')

            return render(request, 'subscription/subscriptions.html', {"subscriptions": subscriptions})

        except AuthenticationFailed:
            return redirect('login')
        except Exception as e:
            message = f"'GET' Method Failed for SubscriptionsView: {e}"
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
            message = f"'PUT' Method Failed for SubscriptionsView: {e}"
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
            message = f"'PATCH' Method Failed for SubscriptionsView: {e}"
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
            message = f"'DELETE' Method Failed for SubscriptionsView: {e}"
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
            message = f"'OPTIONS' Method Failed for SubscriptionsView: {e}"
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
            message = f"'HEAD' Method Failed for SubscriptionsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')