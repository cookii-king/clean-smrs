from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from ...serializers import PriceSerializer
from ...models import Price
from ...config.config import stripe

class PaymentLinksView(APIView):
    def post(self, request):
        try:
            if request.path == "/payment-link/create":
                # Extract the price_id from the POST data
                price_id = request.data.get("price_id")

                if not price_id:
                    return Response({"error": "Price ID is required."}, status=400)

                # Fetch the selected Price
                try:
                    price = Price.objects.get(id=price_id)
                except Price.DoesNotExist:
                    return Response({"error": "Price not found."}, status=404)
                try:
                    # Exclude the CSRF token from the data sent to Stripe
                    stripe_data = {key: value for key, value in request.data.items() if key != "csrfmiddlewaretoken"}

                    # Create the payment link with the cleaned data
                    response = stripe.PaymentLink.create(line_items=[
                        {
                            "price": price.stripe_price_id,  # Stripe Price ID
                            "quantity": 1,  # Default quantity is 1
                        }
                    ],)

                    # Redirect to the Stripe payment link URL
                    return redirect(response.url)
                except Exception as e:
                    raise Exception(f"Failed to create payment link: {str(e)}") from e
            else:
                raise Exception("Invalid URL for POST request")
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PaymentLinksView: {e}"}, status=400)
