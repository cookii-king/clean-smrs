from django.shortcuts import render, redirect
from django.utils.timezone import now, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from ...config.config import stripe
from django.conf import settings
from ...models import Account, Order, Price, Product, OrderItem, Subscription, SubscriptionItem, Plan
import random, string
from django.core.mail import send_mail
from django.http import JsonResponse
import logging
from ...views import authenticate_user, check_mfa


logger = logging.getLogger(__name__)
class WebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            logger.error(f"Invalid payload: {e}")
            return Response({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {e}")
            return Response({"error": "Invalid signature"}, status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            self.handle_checkout_session_completed(event)
        elif event['type'] == 'customer.subscription.created':
            self.handle_subscription_created(event)
        elif event['type'] == 'customer.subscription.updated':
            self.handle_subscription_updated(event)
        elif event['type'] == 'customer.subscription.deleted':
            self.handle_subscription_deleted(event)
        else:
            logger.warning(f"Unhandled event type: {event['type']}")

        # Return a success response for handled events
        return Response({"message": "Webhook processed successfully"}, status=200)

    def handle_checkout_session_completed(self, event):
        session = event['data']['object']
        customer_id = session['customer']
        checkout_id = session['id']
        payment_status = session['payment_status']
        line_items = stripe.checkout.Session.list_line_items(checkout_id)

        if payment_status == 'paid':
            try:
                account = Account.objects.get(stripe_customer_id=customer_id)
                subscription = Subscription.objects.create(
                    customer=account,
                    stripe_subscription_id=session['subscription'],
                    status='active'
                )
                for item in line_items['data']:
                    plan_id = item['price']['id']
                    price_id = item['price']['id']
                    quantity = item['quantity']
                    plan = Plan.objects.get(stripe_plan_id=plan_id)
                    price = Price.objects.get(stripe_price_id=price_id)
                    SubscriptionItem.objects.create(
                        subscription=subscription,
                        plan=plan,
                        price=price,
                        quantity=quantity
                    )
                logger.info(f"Subscription created successfully for customer {account.email}")
            except Account.DoesNotExist:
                logger.error(f"Customer not found for checkout: {customer_id}")
                return Response({"error": "Customer not found"}, status=404)
            except Exception as e:
                logger.error(f"Error creating subscription: {e}")
                return Response({"error": f"Error creating subscription: {e}"}, status=500)

    def handle_subscription_created(self, event):
        subscription_data = event['data']['object']
        customer_id = subscription_data['customer']
        subscription_id = subscription_data['id']
        status = subscription_data['status']

        try:
            account = Account.objects.get(stripe_customer_id=customer_id)
            subscription = Subscription.objects.create(
                customer=account,
                stripe_subscription_id=subscription_id,
                status=status
            )
            for item in subscription_data['items']['data']:
                price_id = item['price']['id']
                quantity = item['quantity']
                price = Price.objects.get(stripe_price_id=price_id)
                SubscriptionItem.objects.create(
                    subscription=subscription,
                    price=price,
                    quantity=quantity,
                    stripe_subscription_item_id=item['id']
                )
            logger.info(f"Subscription created successfully for customer {account.email}")
        except Account.DoesNotExist:
            logger.error(f"Customer not found for subscription: {customer_id}")
            return Response({"error": "Customer not found"}, status=404)
        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            return Response({"error": f"Error creating subscription: {e}"}, status=500)

    def handle_subscription_updated(self, event):
        subscription_data = event['data']['object']
        subscription_id = subscription_data['id']
        status = subscription_data['status']

        try:
            subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
            subscription.status = status
            subscription.save()
            logger.info(f"Subscription updated successfully for subscription ID {subscription_id}")
        except Subscription.DoesNotExist:
            logger.error(f"Subscription not found: {subscription_id}")
            return Response({"error": "Subscription not found"}, status=404)
        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            return Response({"error": f"Error updating subscription: {e}"}, status=500)

    def handle_subscription_deleted(self, event):
        subscription_data = event['data']['object']
        subscription_id = subscription_data['id']

        try:
            subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
            subscription.deleted = now()
            subscription.save()
            logger.info(f"Subscription deleted successfully for subscription ID {subscription_id}")
        except Subscription.DoesNotExist:
            logger.error(f"Subscription not found: {subscription_id}")
            return Response({"error": "Subscription not found"}, status=404)
        except Exception as e:
            logger.error(f"Error deleting subscription: {e}")
            return Response({"error": f"Error deleting subscription: {e}"}, status=500)
    
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
            message = f"'GET' Method Failed for WebhookView: {e}"
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
            message = f"'PUT' Method Failed for WebhookView: {e}"
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
            message = f"'PATCH' Method Failed for WebhookView: {e}"
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
            message = f"'DELETE' Method Failed for WebhookView: {e}"
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
            message = f"'OPTIONS' Method Failed for WebhookView: {e}"
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
            message = f"'HEAD' Method Failed for WebhookView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')