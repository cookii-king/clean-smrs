from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ...models import Checkout, CheckoutLineItem, Account, Cart, Subscription, Plan, Price
from ...config.config import stripe
from ...views import authenticate_user, check_mfa
def handle_response(message, is_error=False, status_code=200):
    return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
class CheckoutView(APIView):

    def post(self, request):
        try:
            account = request.user
            if not account.is_authenticated:
                return handle_response("User is not authenticated.", is_error=True, status_code=401)

            # Check the request path
            if request.path == '/checkout/subscribe':
                return self.handle_subscription(request, account)
            elif request.path == '/checkout/upgrade':
                return self.handle_upgrade(request, account)
            else:
                return self.handle_cart_checkout(request, account)
        except Exception as e:
            return handle_response(f"Failed to process request: {str(e)}", is_error=True, status_code=500)

    def handle_subscription(self, request, account):
        try:
            # Check if the user already has an active subscription
            active_subscription = Subscription.objects.filter(
                customer=account,
                status__in=['active', 'trialing']
            ).first()
            if active_subscription:
                return handle_response(
                    "You already have an active subscription. Please wait until it ends to subscribe to a new plan.",
                    is_error=True,
                    status_code=400
                )

            # Retrieve plan_id or price_id from the request
            plan_id = request.data.get('plan_id')
            price_id = request.data.get('price_id')
            print(f"Plan ID: {plan_id}, Price ID: {price_id}")

            if not plan_id and not price_id:
                return handle_response("Either Plan ID or Price ID is required.", is_error=True, status_code=400)

            # Create a new Checkout instance
            checkout = Checkout.objects.create(
                success_url=request.build_absolute_uri('/checkout/success/'),
                return_url=request.build_absolute_uri('/checkout/failure/'),
                mode='subscription',
                customer=account
            )

            # Add the item to the Checkout
            if plan_id:
                # Check if the plan_id is actually a price_id
                try:
                    plan = Plan.objects.get(stripe_plan_id=plan_id)
                    checkout.add_item(plan_id=plan.stripe_plan_id, quantity=1)
                except Plan.DoesNotExist:
                    # If no Plan is found, try to find a Price
                    price = get_object_or_404(Price, stripe_price_id=plan_id)
                    checkout.add_item(price_id=price.stripe_price_id, quantity=1)
            elif price_id:
                price = get_object_or_404(Price, stripe_price_id=price_id)
                checkout.add_item(price_id=price.stripe_price_id, quantity=1)

            # Create or update the Stripe checkout
            checkout.create_stripe_session()

            # Redirect user to the checkout
            stripe_checkout_url = stripe.checkout.Session.retrieve(checkout.stripe_checkout_id)['url']
            return redirect(stripe_checkout_url)

        except Exception as e:
            return handle_response(f"Failed to handle subscription: {str(e)}", is_error=True, status_code=500)


    def handle_upgrade(self, request, account):
        try:
            new_plan_id = request.data.get('plan_id')
            if not new_plan_id:
                return handle_response("Plan ID is required for upgrade.", is_error=True, status_code=400)

            # Check for an active subscription
            active_subscription = Subscription.objects.filter(
                customer=account,
                status__in=['active', 'trialing']
            ).first()
            if not active_subscription:
                return handle_response("No active subscription found to upgrade.", is_error=True, status_code=400)

            # Retrieve the new plan
            new_plan = get_object_or_404(Plan, stripe_plan_id=new_plan_id)

            # Update the Stripe subscription
            stripe.Subscription.modify(
                active_subscription.stripe_subscription_id,
                items=[{
                    "id": active_subscription.subscription_items.first().stripe_subscription_item_id,
                    "price": new_plan.stripe_plan_id
                }],
                proration_behavior='create_prorations'
            )

            # Update the subscription in your database
            active_subscription.status = 'active'
            active_subscription.save()
            return handle_response("Subscription upgraded successfully.", is_error=False, status_code=200)

        except Exception as e:
            return handle_response(f"Failed to handle upgrade: {str(e)}", is_error=True, status_code=500)

    def handle_cart_checkout(self, request, account):
        try:
            # Fetch the user's cart
            cart = get_object_or_404(Cart, customer=account)
            cart_items = cart.cart_items.all()
            if not cart_items:
                return handle_response("Cart is empty.", is_error=True, status_code=400)

            # Create a new checkout instance
            checkout = Checkout.objects.create(
                success_url=request.build_absolute_uri('/checkout/success/'),
                return_url=request.build_absolute_uri('/checkout/failure/'),
                mode='payment',
                customer=account
            )

            # Add items from the cart to the checkout
            for cart_item in cart_items:
                price = cart_item.product.prices.first()
                if price:
                    checkout.add_item(
                        price_id=price.stripe_price_id,
                        quantity=cart_item.quantity
                    )

            # Create or update the Stripe checkout session
            checkout.create_stripe_session()

            # Clear the cart after successful Stripe session creation
            cart.cart_items.all().delete()

            # Redirect the user to the Stripe checkout URL
            stripe_checkout_url = stripe.checkout.Session.retrieve(checkout.stripe_checkout_id)['url']
            return redirect(stripe_checkout_url)

        except Exception as e:
            return handle_response(f"Failed to handle cart checkout: {str(e)}", is_error=True, status_code=500)
    
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
            message = f"'GET' Method Failed for CheckoutView: {e}"
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
            message = f"'PUT' Method Failed for CheckoutView: {e}"
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
            message = f"'PATCH' Method Failed for CheckoutView: {e}"
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
            message = f"'DELETE' Method Failed for CheckoutView: {e}"
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
            message = f"'OPTIONS' Method Failed for CheckoutView: {e}"
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
            message = f"'HEAD' Method Failed for CheckoutView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')