from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ...serializers import PlanSerializer
from ...models import Plan

class PlanView(APIView):
    def post(self, request):
        try:
            # Check if the request path is for plan creation
            if request.path == '/plan/create':
                try:
                    data = request.data.dict()
                    serializer = PlanSerializer(data=data)
                    if serializer.is_valid():
                        plan = serializer.save()
                        try:
                            stripe_plan = plan.create_in_stripe()
                        except Exception as stripe_error:
                            raise Exception(f"Failed to create Stripe plan: {str(stripe_error)}")
                    else:
                        raise Exception(serializer.errors)
                except Exception as e:
                    raise Exception(f"Failed to create Plan: {str(e)}") from e
            else:
                raise Exception("Invalid URL for POST request")

            # Return a success response
            return Response(data={"message": "Plan created successfully!", "plan_id": stripe_plan["id"]}, status=201)

        except Exception as e:
            # Push the exception to the response
            return Response(data={"error": f"'POST' Method Failed for PlanView: {str(e)}"}, status=400)
   
    def get(self, request, plan_id=None):
        try:
            account = request.user
            if request.path == '/plan/create':
                return render(request, 'create-plan.html', {'account': account})
            else:
                if plan_id is None:  # Handle /plan
                    raise Exception("Plan not found")

                # Handle /plan/<uuid:plan_id>
                account = request.user
                try:
                    plan = Plan.objects.get(id=plan_id)
                except Plan.DoesNotExist as e:
                    raise Exception("Plan not found") from e  # Chain exceptions
                
                return render(request, 'plan.html', {'account': account, "plan": plan})
        except Exception as e:
            # Push the exception to the response
            return Response(data={"error": f"'GET' Method Failed for PlanView: {str(e)}"}, status=400)

class PlansView(APIView):
    def post(self, request):
        try:
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PlansView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            plans = Plan.objects.all()
            return render(request, 'plans.html', {'account':account, "plans": plans})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for PlansView: {e}"}, status=400)
