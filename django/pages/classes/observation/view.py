import requests, os
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from ...models import ApiKey, Subscription
from django.conf import settings
from ...views import authenticate_user, check_mfa

FLASK_URL = os.getenv('FLASK_URL')
FLASK_LOCAL_HOST_URL = os.getenv('FLASK_LOCAL_HOST_URL')

if settings.DEBUG:
    FLASK_URL = FLASK_LOCAL_HOST_URL



class ObservationView(APIView):
    def post(self, request):
        try:
            account = authenticate_user(request)
            check_mfa(account=account)

            # Get the user's primary API key
            api_key = ApiKey.objects.filter(account=account, primary=True).first()
            if not api_key:
                return Response({"error": "No primary API key found"}, status=400)

            # Data from the form submission
            time = request.data.get("time")
            if time and len(time) == 5:  # Only HH:MM (without seconds)
                time = f"{time}:00"  # Append seconds as 00

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
                return render(request, 'observation/create.html', {"message": "Observation created successfully!"})
            else:
                return render(request, 'observation/create.html', {"error": f"Failed to create observation: {response.text}"})

        except AuthenticationFailed:
            return redirect('login')
        except Exception as e:
            return Response({"error": f"'POST' Method Failed for ObservationView: {e}"}, status=500)

    def get(self, request):
        try:
            account = authenticate_user(request)
            check_mfa(account=account)
            if request.path == '/observation/create':
                return render(request, 'observation/create.html')
            return render(request, 'observation/observation.html')
        except AuthenticationFailed:
            return redirect('login')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for ObservationView: {e}", "is_error": True}, status=400)
        except Exception as e:
            message = f"'GET' Method Failed for ObservationView: {e}"
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
            message = f"'PUT' Method Failed for ObservationView: {e}"
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
            message = f"'PATCH' Method Failed for ObservationView: {e}"
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
            message = f"'DELETE' Method Failed for ObservationView: {e}"
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
            message = f"'OPTIONS' Method Failed for ObservationView: {e}"
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
            message = f"'HEAD' Method Failed for ObservationView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

class ObservationsView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            message = "POST request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'POST' Method Failed for ObservationsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')

    def get(self, request):
        try:
            # Authenticate the user
            account = authenticate_user(request)
            check_mfa(account=account)

            # Get the user's primary API key
            api_key = ApiKey.objects.filter(account=account, primary=True).first()
            if not api_key:
                message = "No Primary API key selected in your Account, please either generate a new key or select and set one"
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

        except AuthenticationFailed:
            return redirect('login')
        except Exception as e:
            return render(request, 'system/response.html', {
                'message': f"'GET' Method Failed for ObservationsView: {e}",
                "is_error": True
            }, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            message = "PUT request received"
            is_error = False
            status_code = 201
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')
        except Exception as e:
            message = f"'PUT' Method Failed for ObservationsView: {e}"
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
            message = f"'PATCH' Method Failed for ObservationsView: {e}"
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
            message = f"'DELETE' Method Failed for ObservationsView: {e}"
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
            message = f"'OPTIONS' Method Failed for ObservationsView: {e}"
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
            message = f"'HEAD' Method Failed for ObservationsView: {e}"
            is_error = True
            status_code = 500
            return redirect(f'/response?message={message}&is_error={is_error}&status_code={status_code}')