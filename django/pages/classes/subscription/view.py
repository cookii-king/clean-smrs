from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from ...models import Plan, Subscription, Account

class SubscriptionView(APIView):
    def post(self, request):
            try:
                if request.path == '/subscription/cancel':
                    subscription_id = request.data.get('subscription_id')
                    subscription = Subscription.objects.filter(id=subscription_id).first()

                    if not subscription:
                        return Response({"error": "Subscription not found."}, status=404)

                    subscription.cancel_subscription()
                    return redirect('subscriptions')

                return Response({"error": "Invalid action."}, status=400)
            except Exception as e:
                return Response({"error": f"Failed to cancel subscription: {e}"}, status=400)
            
    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'subscription/subscription.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for SubscriptionView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for SubscriptionView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for SubscriptionView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for SubscriptionView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for SubscriptionView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for SubscriptionView: {e}"}, status=400)

class SubscriptionsView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for SubscriptionsView: {e}"}, status=400)

    def get(self, request):
        try:
            user = request.user
            account = Account.objects.filter(id=user.id).first()
            # Fetch all subscriptions (active and inactive) for the user
            # subscriptions = Subscription.objects.all()
            subscriptions = Subscription.objects.filter(customer=account.stripe_customer_id).select_related('customer').prefetch_related('subscription_items__price', 'subscription_items__plan')
            # subscriptions = Subscription.objects.filter(
            #        customer=account.stripe_customer_id, deleted__isnull=True, status='active' 
            #     ).all()
            return render(request, 'subscription/subscriptions.html', {"subscriptions": subscriptions})
        except Exception as e:
            return render(request, 'subscription/subscriptions.html', {"error": f"Error fetching subscriptions: {e}"})
    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for SubscriptionsView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for SubscriptionsView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for SubscriptionsView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for SubscriptionsView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for SubscriptionsView: {e}"}, status=400)
