from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from ...models import Plan, Subscription, ApiKey
import requests, os
from django.conf import settings

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..authentication.view import JWTAuthentication, IsAuthenticated, LoginRequiredMixin, AuthenticationFailed


FLASK_URL = os.getenv('FLASK_URL')
FLASK_LOCAL_HOST_URL = os.getenv('FLASK_LOCAL_HOST_URL')

if settings.DEBUG:
    FLASK_URL = FLASK_LOCAL_HOST_URL


class ObservationView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    def check_mfa(self, account):
        if not account.mfa_confirmed and account.mfa_enabled:
              return redirect("verify-mfa")
    # @method_decorator(login_required)
    def post(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Get the user's primary API key
            api_key = ApiKey.objects.filter(account=request.user, primary=True).first()
            if not api_key:
                return Response({"error": "No primary API key found"}, status=400)

            # Data from the form submission
            time = request.data.get("time")
            # Ensure the time format is HH:MM:SS
            if time and len(time) == 5:  # Only HH:MM (without seconds)
                time = f"{time}:00"  # Append seconds as 00

            # Data from the form submission
            data = {
                "date": request.data.get("date"),
                "time": time,
                "time_zone_offset": request.data.get("time_zone_offset"),
                "latitude": request.data.get("latitude"),
                "longitude": request.data.get("longitude"),
                "temperature_water": request.data.get("temperature_water"),
                "temperature_air": request.data.get("temperature_air"),
                "humidity": request.data.get("humidity"),
                "wind_speed": request.data.get("wind_speed"),
                "wind_direction": request.data.get("wind_direction"),
                "precipitation": request.data.get("precipitation"),
                "haze": request.data.get("haze"),
                "becquerel": request.data.get("becquerel"),
                "notes": request.data.get("notes"),
            }

            # API endpoint
            url = f"{FLASK_URL}/observation/create"
            headers = {
                "Content-Type": "application/json",
                "X-API-KEY": api_key.key,
            }

            # Make POST request to the external API
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 201:
                # On success, redirect back to the form with a success message
                return render(
                    request, 
                    'observation/create.html', 
                    {"message": "Observation created successfully!"}
                )
            else:
                # Handle errors from the external API
                return render(
                    request, 
                    'observation/create.html', 
                    {"error": f"Failed to create observation: {response.text}"}
                )
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'POST' Method Failed for ObservationView: {e}", "is_error": True}, status=500)
            return Response(data={"error": f"'POST' Method Failed for ObservationView: {e}", "is_error": True}, status=500)
            
    # @method_decorator(login_required)
    def get(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            if request.path == '/observation/create':
                return render(request, 'observation/create.html')
            # Handle GET requests
            return render(request, 'observation/observation.html')
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
            # return Response(data={"error": f"'GET' Method Failed for ObservationView: {e}", "is_error": True}, status=500)
            
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'PUT' Method Failed for ObservationView: {e}", "is_error": True}, status=500)
            return Response(data={"error": f"'PUT' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
            
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'PATCH' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
            return Response(data={"error": f"'PATCH' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'DELETE' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
            return Response(data={"error": f"'DELETE' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'OPTIONS' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
            return Response(data={"error": f"'OPTIONS' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'HEAD' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
            return Response(data={"error": f"'HEAD' Method Failed for ObservationView: {e}", "is_error": True}, status=400)

class ObservationsView(APIView):
    def authenticate_user(self, request):
        """Authenticate the user using JWT and return the account."""
        jwt_auth = JWTAuthentication()
        account, _ = jwt_auth.authenticate(request)
        if account is None:
            raise AuthenticationFailed('Authentication failed')
        return account
    def check_mfa(self, account):
        if not account.mfa_confirmed and account.mfa_enabled:
              return redirect("verify-mfa")
    # @method_decorator(login_required)
    def post(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'POST' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
            return Response(data={"error": f"'POST' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
    # @method_decorator(login_required)
    def get(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)

            # Get the user's primary API key
            api_key = ApiKey.objects.filter(account=account, primary=True).first()
            message = None
            if not api_key:
                message = "No Primary API key selected in your Account, please either generate a new key or select and set one"
                # Return early if there's no API key
                return render(request, 'observation/observations.html', {"observations": [], "message": message})

            # Check if the user has an active subscription
            subscription = Subscription.objects.filter(customer=account, status='active', deleted__isnull=True).first()
            if not subscription:
                message = "You need to subscribe to access this feature"
                return render(request, 'observation/observations.html', {"observations": [], "message": message})

            # Fetch observations from the external API
            url = f"{FLASK_URL}/observations"
            headers = {
                "X-API-KEY": api_key.key,
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                observations = response.json()
                return render(request, 'observation/observations.html', {"observations": observations})
            else:
                message = f"Failed to fetch observations: {response.text}"
                return render(request, 'observation/observations.html', {"observations": [], "message": message})

        except AuthenticationFailed as e:
            return redirect('login')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
            # return Response(data={"error": f"'GET' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
    # @method_decorator(login_required)
    def put(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'PUT' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
            return Response(data={"error": f"'PUT' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
    # @method_decorator(login_required)
    def patch(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'PATCH' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
            return Response(data={"error": f"'PATCH' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
    # @method_decorator(login_required)
    def delete(self, request):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            # return render(request, 'system/response.html', {'message': f"'PATCH' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
            return Response(data={"error": f"'DELETE' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
    # @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)
    # @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            account = self.authenticate_user(request)
            self.check_mfa(account=account)
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except AuthenticationFailed as e:
            return redirect('login')  
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for ObservationsView: {e}", "is_error": True}, status=400)