from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from ...models import Checkout, CheckoutLineItem, Plan, Price, Cart, Subscription, Order
from ...config.config import stripe
 

class CheckoutView(APIView):
    def post(self, request):
        try:
            account = request.user
            print(f"path: {request.path}")

            if request.path == '/checkout/subscribe':
                # Check if the user already has an active subscription
                active_subscription = Subscription.objects.filter(
                    customer=account,
                    status__in=['active', 'trialing']  # Include statuses indicating an active subscription
                ).first()
                if active_subscription:
                    return Response({
                        "error": "You already have an active subscription. Please wait until it ends to subscribe to a new plan."
                    }, status=400)

                plan_id = request.data.get('plan_id')
                if not plan_id:
                    return Response({"error": "Plan ID is required."}, status=400)

                # Retrieve the plan
                plan = Plan.objects.get(stripe_plan_id=plan_id)

                # Create or retrieve the Checkout instance
                checkout = Checkout.objects.create(
                    success_url=request.build_absolute_uri('/checkout/success/'),
                    return_url=request.build_absolute_uri('/checkout/failure/'),
                    mode=request.data.get('mode'),
                    customer=account
                )

                # Add the item to the Checkout
                checkout.add_item(plan_id=plan.stripe_plan_id, quantity=1)

                # Create or update the Stripe checkout
                checkout.create_or_update_stripe_checkout()

                # Retrieve the Stripe checkout session ID
                stripe_checkout_id = checkout.stripe_checkout_id

                # # Update the success URL to include the session_id
                # success_url = request.build_absolute_uri(f'/checkout/success/?session_id={stripe_checkout_id}')
                # checkout.success_url = success_url
                # checkout.save()

                # Redirect user to the checkout
                stripe_checkout_url = stripe.checkout.Session.retrieve(checkout.stripe_checkout_id)['url']
                return redirect(stripe_checkout_url)

            elif request.path == '/checkout/upgrade':
                new_plan_id = request.data.get('plan_id')
                if not new_plan_id:
                    return Response({"error": "Plan ID is required for upgrade."}, status=400)

                # Check for an active subscription
                active_subscription = Subscription.objects.filter(
                    customer=account,
                    status__in=['active', 'trialing']
                ).first()

                if not active_subscription:
                    return Response({
                        "error": "No active subscription found to upgrade."
                    }, status=400)

                # Retrieve the new plan
                new_plan = Plan.objects.get(stripe_plan_id=new_plan_id)

                # Update the Stripe subscription
                stripe.Subscription.modify(
                    active_subscription.stripe_subscription_id,
                    items=[{
                        "id": active_subscription.subscription_items.first().stripe_subscription_item_id,
                        "price": new_plan.stripe_plan_id
                    }],
                    proration_behavior='create_prorations'  # Automatically calculate cost differences
                )

                # Update the subscription in your database
                active_subscription.status = 'active'
                active_subscription.save()

                return Response({"message": "Subscription upgraded successfully."}, status=200)

            else:
                # Fetch the user's cart
                cart = account.cart
                cart_items = cart.cart_items.all()

                if not cart_items:
                    return Response({"error": "Cart is empty."}, status=400)

                # Create a new checkout instance
                checkout = Checkout.objects.create(
                    success_url=request.build_absolute_uri('/checkout/success/'),
                    return_url=request.build_absolute_uri('/checkout/failure/'),
                    mode='payment',  # Adjust based on your mode (payment/subscription)
                    customer=account
                )

                # Add items from the cart to the checkout
                for cart_item in cart_items:
                    price_id = Price.objects.filter(product=cart_item.product).first()
                    checkout.add_item(
                        price_id=price_id.stripe_price_id,  # Assuming each product has a stripe price ID
                        quantity=cart_item.quantity
                    )

                # Create or update the Stripe checkout session
                checkout.create_or_update_stripe_checkout()

                # Retrieve the Stripe checkout session ID
                stripe_checkout_id = checkout.stripe_checkout_id

                # # Update the success URL to include the session_id
                # success_url = request.build_absolute_uri(f'/checkout/success/?session_id={stripe_checkout_id}')
                # checkout.success_url = success_url
                # checkout.save()

                # Clear the cart after successful Stripe session creation
                cart.clear_cart()

                # Redirect the user to the Stripe checkout URL
                stripe_checkout_url = stripe.checkout.Session.retrieve(checkout.stripe_checkout_id)['url']
                return redirect(stripe_checkout_url)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found for the user."}, status=404)
        except Exception as e:
            return Response({"error": f"Failed to create checkout session: {str(e)}"}, status=500)

    def get(self, request):
        try:
            if request.path in ['/checkout/success', '/checkout/success/']:
                # Retrieve the Checkout ID from the query parameters
                checkout_id = request.GET.get('checkout')
                if not checkout_id:
                    return render(request, 'checkout/success.html', {"error": "Checkout ID not provided"})

                # Fetch the related order using the checkout ID
                checkout = get_object_or_404(Checkout, id=checkout_id)
                order = get_object_or_404(Order, checkout=checkout)

                return render(request, 'checkout/success.html', {'order': order})

            if request.path in ['/checkout/failure', '/checkout/failure/']:
                return render(request, 'checkout/failure.html')

            return Response({"message": "GET request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for CheckoutView: {e}"}, status=400)


    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for CheckoutView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for CheckoutView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for CheckoutView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for CheckoutView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for CheckoutView: {e}"}, status=400)
    
class CheckoutsView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for CheckoutsView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            checkouts = Checkout.objects.all()
            return render(request, 'checkout/checkouts.html', {"checkouts": checkouts})
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for CheckoutsView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for CheckoutsView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for CheckoutsView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for CheckoutsView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for CheckoutsView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for CheckoutsView: {e}"}, status=400)
        
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.shortcuts import render, redirect
# from ...models import Checkout, CheckoutLineItem, Plan
# from ...config.config import stripe

# class CheckoutView(APIView):
#     def post(self, request):
#         try:
#             account = request.user
#             if request.path == '/checkout/create':
#                 plan_id = request.data.get('plan_id')
#                 if not plan_id:
#                     return Response({"error": "Plan ID is required."}, status=400)

#                 # Retrieve the plan
#                 plan = Plan.objects.get(stripe_plan_id=plan_id)

#                 # Create or retrieve the Checkout instance
#                 checkout = Checkout.objects.create(
#                     success_url=request.build_absolute_uri('/checkout/success/'),
#                     return_url=request.build_absolute_uri('/checkout/failure/'),
#                     mode=request.data.get('mode'),
#                     customer=account
#                 )

#                 # Add the item to the Checkout
#                 checkout.add_item(plan_id=plan.stripe_plan_id, quantity=1)

#                 # Create or update the Stripe checkout
#                 checkout.create_or_update_stripe_checkout()

#                 # Redirect user to the checkout
#                 stripe_checkout_url = stripe.checkout.Session.retrieve(checkout.stripe_checkout_id)['url']
#                 return redirect(stripe_checkout_url)

#             return Response({"message": "Invalid action."}, status=400)

#         except Plan.DoesNotExist:
#             return Response({"error": "Plan not found."}, status=404)
#         except Exception as e:
#             return Response(data={"error": f"Failed to create checkout: {e}"}, status=500)
        
#     def get(self, request):
#         try:
#             if request.path == '/checkout/success':
#                 return render(request, 'checkout/success.html')
#             if request.path == '/checkout/failure':
#                 return render(request, 'checkout/failure.html')
#             if request.path == '/checkout/success/':
#                 return render(request, 'checkout/success.html')
#             if request.path == '/checkout/failure/':
#                 return render(request, 'checkout/failure.html')
#             # Handle GET requests
#             return render(request, 'checkout/checkout.html')
#         except Exception as e:
#                     return Response(data={"error": f"'GET' Method Failed for CheckoutView: {e}"}, status=400)

#     def put(self, request):
#         try:
#             # Handle PUT requests
#             return Response({"message": "PUT request received"}, status=201)
#         except Exception as e:
#             return Response(data={"error": f"'PUT' Method Failed for CheckoutView: {e}"}, status=400)

#     def patch(self, request):
#         try:
#             # Handle PATCH requests
#             return Response({"message": "PATCH request received"}, status=200)
#         except Exception as e:
#             return Response(data={"error": f"'PATCH' Method Failed for CheckoutView: {e}"}, status=400)

#     def delete(self, request):
#         try:
#             # Handle DELETE requests
#             return Response({"message": "DELETE request received"}, status=200)
#         except Exception as e:
#             return Response(data={"error": f"'DELETE' Method Failed for CheckoutView: {e}"}, status=400)

#     def options(self, request, *args, **kwargs):
#         try:
#             # Handle OPTIONS requests
#             return Response({"message": "OPTIONS request received"}, status=204)
#         except Exception as e:
#             return Response(data={"error": f"'OPTIONS' Method Failed for CheckoutView: {e}"}, status=400)

#     def head(self, request, *args, **kwargs):
#         try:
#             # Handle HEAD requests
#             # Since Django automatically handles HEAD, no implementation is required
#             # The HEAD response will be the same as GET but without the body
#             return Response({"message": "HEAD request received"}, status=200)
#         except Exception as e:
#             return Response(data={"error": f"'HEAD' Method Failed for CheckoutView: {e}"}, status=400)
    

