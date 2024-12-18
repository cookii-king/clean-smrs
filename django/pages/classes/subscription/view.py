from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ...serializers import SubscriptionSerializer
from ...models import Subscription

class SubscriptionView(APIView):
    def post(self, request):
        stripe_subscription = None
        try:
            # Check if the request path is for subscription creation
            if request.path == '/subscription/create':
                try:
                    data = request.data.dict()

                    # Extract and reconstruct 'items' list
                    items = []
                    for key, value in data.items():
                        if key.startswith("items[") and key.endswith("][price]"):
                            index = int(key.split('[')[1].split(']')[0])
                            while len(items) <= index:
                                items.append({})
                            items[index]["price"] = value

                    data["items"] = items  # Add items back into the payload

                    print(f"Reconstructed data: {data}")  # Debugging: Verify payload structure

                    # Serialize and save subscription
                    serializer = SubscriptionSerializer(data=data)
                    if serializer.is_valid():
                        subscription = serializer.save()
                        stripe_subscription = subscription.create_in_stripe()
                    else:
                        raise Exception(serializer.errors)
                except Exception as e:
                    raise Exception(f"Failed to create subscription: {str(e)}") from e
            else:
                raise Exception("Invalid URL for POST request")

            # Return a success response
            return Response(
                data={
                    "message": "Subscription created successfully!",
                    "subscription_id": stripe_subscription["id"]
                },
                status=201
            )
        except Exception as e:
            return Response(
                data={"error": f"'POST' Method Failed for SubscriptionView: {str(e)}"},
                status=400
            )
    def get(self, request, subscription_id=None):
        try:
            account = request.user
            if request.path == '/subscription/create':
                return render(request, 'create-subscription.html', {'account': account})
            else:
                if subscription_id is None:  # Handle /subscription
                    raise Exception("Subscription not found")

                # Handle /subscription/<uuid:subscription_id>
                account = request.user
                try:
                    subscription = Subscription.objects.get(id=subscription_id)
                except Subscription.DoesNotExist as e:
                    raise Exception("Subscription not found") from e  # Chain exceptions
                
                return render(request, 'subscription.html', {'account': account, "subscription": subscription})
        except Exception as e:
            # Push the exception to the response
            return Response(data={"error": f"'GET' Method Failed for SubscriptionView: {str(e)}"}, status=400)

class SubscriptionsView(APIView):
    def post(self, request):
        try:
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for SubscriptionsView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            subscriptions = Subscription.objects.all()
            return render(request, 'subscriptions.html', {'account':account, "subscriptions": subscriptions})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for SubscriptionsView: {e}"}, status=400)
