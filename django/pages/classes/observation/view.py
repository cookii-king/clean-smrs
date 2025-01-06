from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from ...models import Plan, Subscription, ApiKey
import requests, os
from django.conf import settings

FLASK_URL = os.getenv('FLASK_URL')
FLASK_LOCAL_HOST_URL = os.getenv('FLASK_LOCAL_HOST_URL')

if settings.DEBUG:
    FLASK_URL = FLASK_LOCAL_HOST_URL


class ObservationView(APIView):
    def post(self, request):
        try:
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
            url = f"f{FLASK_URL}/observation/create"
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
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for ObservationView: {e}"}, status=500)
        
    def get(self, request):
        try:
            if request.path == '/observation/create':
                return render(request, 'observation/create.html')
            # Handle GET requests
            return render(request, 'observation/observation.html')
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for ObservationView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for ObservationView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for ObservationView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for ObservationView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for ObservationView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for ObservationView: {e}"}, status=400)

class ObservationsView(APIView):
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for ObservationsView: {e}"}, status=400)

    def get(self, request):
        try:
            # Get the user's primary API key
            api_key = ApiKey.objects.filter(account=request.user, primary=True).first()
            if not api_key:
                return Response({"error": "No primary API key found"}, status=400)

            # Check if the user has an active subscription
            subscription = Subscription.objects.filter(customer=request.user,                     status='active',
                    deleted__isnull=True).first()
            # if not subscription:
            #     return Response({"error": "You need to subscribe to access this feature"}, status=403)

            url = f"{FLASK_URL}/observations"
            headers = {
                "X-API-KEY": api_key.key,
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                observations = response.json()
                return render(request, 'observation/observations.html', {"observations": observations})
            else:
                return render(request, 'observation/observations.html', {"observations": []})

        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for ObservationsView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for ObservationsView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for ObservationsView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for ObservationsView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for ObservationsView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for ObservationsView: {e}"}, status=400)