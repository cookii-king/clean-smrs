from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from ...models import PaymentLink, PaymentLinkLineItem, Plan
from ...config.config import stripe

class PaymentLinkView(APIView):
    def post(self, request):
        try:
            if request.path == '/payment-link/create':
                plan_id = request.data.get('plan_id')
                if not plan_id:
                    return Response({"error": "Plan ID is required."}, status=400)

                # Retrieve the plan
                plan = Plan.objects.get(stripe_plan_id=plan_id)

                # Create or retrieve the PaymentLink instance
                payment_link = PaymentLink.objects.create()

                # Add the item to the PaymentLink
                payment_link.add_item(plan_id=plan.stripe_plan_id, quantity=1)

                # Create or update the Stripe payment link
                payment_link.create_or_update_stripe_payment_link()

                # Redirect user to the payment link
                stripe_payment_link_url = stripe.PaymentLink.retrieve(payment_link.stripe_payment_link_id)['url']
                return redirect(stripe_payment_link_url)

            return Response({"message": "Invalid action."}, status=400)

        except Plan.DoesNotExist:
            return Response({"error": "Plan not found."}, status=404)
        except Exception as e:
            return Response(data={"error": f"Failed to create payment link: {e}"}, status=500)
        
    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'payment-link/payment-link.html')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for PaymentLinkView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for PaymentLinkView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for PaymentLinkView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for PaymentLinkView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for PaymentLinkView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for PaymentLinkView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for PaymentLinkView: {e}"}, status=400)
    

class PaymentLinksView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PaymentLinksView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            payment_links = PaymentLink.objects.all()
            return render(request, 'payment-link/payment-links.html', {"payment-links": payment_links})
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for PaymentLinksView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for PaymentLinksView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for PaymentLinksView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for PaymentLinksView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for PaymentLinksView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for PaymentLinksView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for PaymentLinksView: {e}"}, status=400)