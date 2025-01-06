from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from ...models import Webhook
from django.conf import settings
import stripe

class WebhookView(APIView):
    def post(self, request):
        try:
            stripe_data = request.body  # Parse raw body data
            sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
            stripe_endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

            # Construct the Stripe event
            stripe_event = stripe.Webhook.construct_event(
                payload=stripe_data,  # Pass the raw payload
                sig_header=sig_header,
                secret=stripe_endpoint_secret
            )

            stripe_event_id = stripe_event['id']
            stripe_event_type = stripe_event['type']
            stripe_event_data = stripe_event['data']

            # Check if the event has already been processed
            if Webhook.objects.filter(event_id=stripe_event_id).exists():
                return Response({"message": "Event already processed"}, status=200)

            # Create a new webhook record
            webhook = Webhook.objects.create(
                event_id=stripe_event_id,
                event_type=stripe_event_type,
                data=stripe_event_data
            )
            webhook.process_event()
            return Response({"message": "Webhook processed successfully"}, status=200)

        except stripe.error.SignatureVerificationError as e:
            # Handle signature verification errors
            print(f"Webhook signature verification failed: {str(e)}")
            return Response({"error": "Invalid signature"}, status=400)
        except Exception as e:
            # Handle other exceptions
            print(f"Error processing webhook: {str(e)}")
            return Response({"error": f"Error processing webhook: {e}"}, status=400)
        
    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'webhook/webhook.html')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for WebhookView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for WebhookView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for WebhookView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for WebhookView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for WebhookView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for WebhookView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for WebhookView: {e}"}, status=400)
