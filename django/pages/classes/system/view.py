from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from ...models import Plan, Subscription

class IndexView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for IndexView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'system/index.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for IndexView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for IndexView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for IndexView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for IndexView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for IndexView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for IndexView: {e}"}, status=400)

class AboutView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for AboutView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'system/about.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for AboutView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for AboutView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for AboutView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for AboutView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for AboutView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for AboutView: {e}"}, status=400)

class ContactView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for ContactView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'system/contact.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for ContactView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for ContactView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for ContactView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for ContactView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for ContactView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for ContactView: {e}"}, status=400)

class SupportView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for SupportView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'system/support.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for SupportView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for SupportView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for SupportView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for SupportView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for SupportView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for SupportView: {e}"}, status=400)

class TermsOfServiceView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for TermsOfServiceView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'system/terms-of-service.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for TermsOfServiceView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for TermsOfServiceView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for TermsOfServiceView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for TermsOfServiceView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for TermsOfServiceView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for TermsOfServiceView: {e}"}, status=400)


class PrivacyPolicyView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PrivacyPolicyView: {e}"}, status=400)

    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'system/privacy-policy.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for PrivacyPolicyView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for PrivacyPolicyView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for PrivacyPolicyView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for PrivacyPolicyView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for PrivacyPolicyView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for PrivacyPolicyView: {e}"}, status=400)


class PlansAndPricingView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PlansAndPricingView: {e}"}, status=400)

    # def get(self, request):
    #     try:
    #         # Handle GET requests
    #         account = request.user
    #         subscriptions = Subscription.objects.filter(customer=account.stripe_customer_id).all()
    #         # Fetch plans and group by interval
    #         monthly_plans = Plan.objects.filter(interval='month').all()
    #         yearly_plans = Plan.objects.filter(interval='year').all()
    #         monthly_plans_subscription_counts = {plan.stripe_plan_id: 0 for plan in monthly_plans}
    #         yearly_plans_subscription_counts = {plan.stripe_plan_id: 0 for plan in yearly_plans}

    #         # Calculate the subscription count for each plan
    #         for subscription in subscriptions:
    #             for item in subscription.items:
    #                 plan_id = item.get('price')
    #                 if plan_id in monthly_plans_subscription_counts:
    #                        monthly_plans_subscription_counts[plan_id] += 1
    #                 if plan_id in yearly_plans_subscription_counts:
    #                        yearly_plans_subscription_counts[plan_id] += 1
    #         # Render the template with plans
    #         return render(request, 'system/plans-and-pricing.html', {
    #             'monthly_plans': monthly_plans,
    #             'yearly_plans': yearly_plans,
    #             "subscriptions": subscriptions, 
    #             'monthly_plans_subscription_counts': monthly_plans_subscription_counts,
    #             'yearly_plans_subscription_counts': yearly_plans_subscription_counts,
    #         })
    #     except Exception as e:
    #                 return Response(data={"error": f"'GET' Method Failed for PlansAndPricingView: {e}"}, status=400)

    def get(self, request):
        try:
            account = request.user
            subscriptions = Subscription.objects.filter(customer=account.stripe_customer_id).all()
            monthly_plans = Plan.objects.filter(interval='month').all()
            yearly_plans = Plan.objects.filter(interval='year').all()

            # Add subscription counts and durations
            monthly_plans_subscription_data = {}
            yearly_plans_subscription_data = {}

            for subscription in subscriptions:
                for item in subscription.get_items():
                    plan_id = item.price.stripe_price_id
                    duration = subscription.subscription_duration()

                    if plan_id in monthly_plans_subscription_data:
                        monthly_plans_subscription_data[plan_id]['count'] += 1
                        monthly_plans_subscription_data[plan_id]['durations'].append(duration)
                    elif plan_id in yearly_plans_subscription_data:
                        yearly_plans_subscription_data[plan_id]['count'] += 1
                        yearly_plans_subscription_data[plan_id]['durations'].append(duration)

            active_subscription = Subscription.objects.filter(
                customer=account,
                status__in=['active', 'trialing']
            ).first()

            return render(request, 'system/plans-and-pricing.html', {
                'monthly_plans': monthly_plans,
                'yearly_plans': yearly_plans,
                "subscriptions": subscriptions,
                'monthly_plans_subscription_data': monthly_plans_subscription_data,
                'yearly_plans_subscription_data': yearly_plans_subscription_data,
                'active_subscription': active_subscription,
            })
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for PlansAndPricingView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for PlansAndPricingView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for PlansAndPricingView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for PlansAndPricingView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for PlansAndPricingView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for PlansAndPricingView: {e}"}, status=400)