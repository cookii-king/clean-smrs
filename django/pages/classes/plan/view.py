from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from ...models import Plan
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..authentication.view import JWTAuthentication, IsAuthenticated, LoginRequiredMixin, AuthenticationFailed

class PlanView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    # @method_decorator(login_required)
    def post(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PlanView: {e}"}, status=400)
    # @method_decorator(login_required)
    def get(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle GET requests
           # Fetch plans and group by interval
            monthly_plans = Plan.objects.filter(interval='month')
            yearly_plans = Plan.objects.filter(interval='year')

            # Render the template with plans
            return render(request, 'plan/plan.html')
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for PlanView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for PlanView: {e}"}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for PlanView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for PlanView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for PlanView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for PlanView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for PlanView: {e}"}, status=400)
    

class PlansView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    # @method_decorator(login_required)
    def post(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PlansView: {e}"}, status=400)
    # @method_decorator(login_required)
    def get(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle GET requests
           # Fetch plans and group by interval
            plans = Plan.objects.all()
            # Render the template with plans
            return render(request, 'plan/plans.html', {"plans": plans})
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for PlansView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for PlansView: {e}"}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for PlansView: {e}"}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for PlansView: {e}"}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for PlansView: {e}"}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for PlansView: {e}"}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login') 
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for PlansView: {e}"}, status=400)