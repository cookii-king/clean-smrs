from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from ...models import Plan, Subscription, Account
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..authentication.view import JWTAuthentication, IsAuthenticated, LoginRequiredMixin, AuthenticationFailed

class SubscriptionView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    # @method_decorator(login_required)
    def post(self, request):
            try:
                account = self.authenticate_user(request)
                if request.path == '/subscription/cancel':
                    subscription_id = request.data.get('subscription_id')
                    subscription = Subscription.objects.filter(id=subscription_id).first()

                    if not subscription:
                        return Response({"error": "Subscription not found."}, status=404)

                    subscription.cancel_subscription()
                    return redirect('subscriptions')

                return Response({"error": "Invalid action."}, status=400)
            except AuthenticationFailed as e:
                return redirect('login')
            except Exception as e:
                return Response({"error": f"Failed to cancel subscription: {e}"}, status=400)
    # @method_decorator(login_required)      
    def get(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle GET requests
            return render(request, 'subscription/subscription.html')
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for SubscriptionView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for SubscriptionView: {e}"}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for SubscriptionView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for SubscriptionView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for SubscriptionView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for SubscriptionView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for SubscriptionView: {e}"}, status=400)

class SubscriptionsView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    # @method_decorator(login_required)
    def post(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for SubscriptionsView: {e}"}, status=400)
    # @method_decorator(login_required)
    def get(self, request):
        try:
            account = self.authenticate_user(request)
            user = request.user
            account = Account.objects.filter(id=user.id).first()
            # Fetch all subscriptions (active and inactive) for the user
            # subscriptions = Subscription.objects.all()
            subscriptions = Subscription.objects.filter(customer=account.stripe_customer_id).select_related('customer').prefetch_related('subscription_items__price', 'subscription_items__plan')
            # subscriptions = Subscription.objects.filter(
            #        customer=account.stripe_customer_id, deleted__isnull=True, status='active' 
            #     ).all()
            return render(request, 'subscription/subscriptions.html', {"subscriptions": subscriptions})
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return render(request, 'subscription/subscriptions.html', {"error": f"Error fetching subscriptions: {e}"})
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for SubscriptionsView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for SubscriptionsView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for SubscriptionsView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for SubscriptionsView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
                return redirect('login')
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for SubscriptionsView: {e}"}, status=400)
