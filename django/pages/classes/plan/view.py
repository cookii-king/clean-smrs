from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from ...models import Plan
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
class PlanView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PlanView: {e}"}, status=400)
    @method_decorator(login_required)
    def get(self, request):
        try:
            # Handle GET requests
           # Fetch plans and group by interval
            monthly_plans = Plan.objects.filter(interval='month')
            yearly_plans = Plan.objects.filter(interval='year')

            # Render the template with plans
            return render(request, 'plan/plan.html')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for PlanView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for PlanView: {e}"}, status=400)
    @method_decorator(login_required)
    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for PlanView: {e}"}, status=400)
    @method_decorator(login_required)
    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for PlanView: {e}"}, status=400)
    @method_decorator(login_required)
    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for PlanView: {e}"}, status=400)
    @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for PlanView: {e}"}, status=400)
    @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for PlanView: {e}"}, status=400)
    

class PlansView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PlansView: {e}"}, status=400)
    @method_decorator(login_required)
    def get(self, request):
        try:
            # Handle GET requests
           # Fetch plans and group by interval
            plans = Plan.objects.all()
            # Render the template with plans
            return render(request, 'plan/plans.html', {"plans": plans})
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for PlansView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for PlansView: {e}"}, status=400)
    @method_decorator(login_required)
    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for PlansView: {e}"}, status=400)
    @method_decorator(login_required)
    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for PlansView: {e}"}, status=400)
    @method_decorator(login_required)
    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for PlansView: {e}"}, status=400)
    @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for PlansView: {e}"}, status=400)
    @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for PlansView: {e}"}, status=400)