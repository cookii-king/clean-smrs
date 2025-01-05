from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from ...models import ApiKey
from django.utils.timezone import now
from ...models import Account, Subscription

class ApiKeyView(APIView):
    def post(self, request):
        try:
            user = request.user
            account = Account.objects.filter(id=user.id).first()
            # Differentiate the functionality based on the request path
            if request.path in ['/api-key/validate', '/api-key/validate/']:
                # Validate API Key logic
                api_key = request.data.get('api_key')
                if not api_key:
                    return Response({"error": "No API Key Provided."}, status=400)

                key = ApiKey.objects.filter(key=api_key, active=True).first()
                if not key:
                    return Response({"error": "Invalid API Key Provided."}, status=404)

                caller_account = Account.objects.filter(id=key.account.id).first()
                if not caller_account:
                    return Response({"error": "Could not find who did it."}, status=404)
                
                # Check if the account has an active subscription
                subscription = Subscription.objects.filter(
                    customer=caller_account.stripe_customer_id,
                    status='active',
                    deleted__isnull=True
                ).first()

                if not subscription:
                    return Response({"error": "No active subscription found. Please subscribe to use the API."}, status=403)


                print(f"Who is requesting? Account: ${caller_account.username}")
                
                # Reset credits if the reset date has passed
                if key.reset_date <= now():
                    key.reset_credits()

                # Check if the credit limit has been reached
                if key.credits_used >= key.credit_limit:
                    return Response({"error": "Credit limit reached."}, status=403)

                # Increment credit usage and save
                key.credits_used += 1
                key.save()

                return Response({"message": "API Key validated successfully."}, status=200)

            elif request.path in ['/api-key/generate', '/api-key/generate/']:
                # Generate API Key logic
                if not account:
                    return Response({"error": "Invalid account ID."}, status=404)

                # Generate a new API key
                new_api_key = ApiKey.objects.create(account=account)
                new_api_key.generate_key()

                return Response({"message": "API Key generated successfully."}, status=201)
            

            elif request.path in ['/api-key/re-generate', '/api-key/re-generate/']:
                api_id = request.data.get('api_id')
                if not api_id:
                    return Response({"error": "No API ID Provided."}, status=400)

                key = ApiKey.objects.filter(id=api_id, active=True).first()
                if not key:
                    return Response({"error": "Invalid API ID Provided."}, status=404)

                # Regenerate the key and return it
                new_key = key.regenerate_key()
                return Response({"api_key": new_key}, status=200)

            elif request.path in ['/api-key/reveal', '/api-key/reveal/']:
                api_id = request.data.get('api_id')
                if not api_id:
                    return Response({"error": "No API ID Provided."}, status=400)

                key = ApiKey.objects.filter(id=api_id, active=True).first()
                if not key:
                    return Response({"error": "Invalid API ID Provided."}, status=404)

                # Always return the key if it's revealed
                revealed_key = key.reveal() if not key.revealed else key.key
                return Response({"api_key": revealed_key}, status=200)
            
            elif request.path in ['/api-key/set-primary', '/api-key/set-primary/']:
                api_id = request.data.get('key_id')
                if not api_id:
                    return Response({"error": "No API ID Provided."}, status=400)

                key = ApiKey.objects.filter(id=api_id, active=True).first()
                if not key:
                    return Response({"error": "Invalid API ID Provided."}, status=404)

                # Set the selected API key as primary
                ApiKey.objects.filter(account=key.account).update(primary=False)
                key.primary = True
                key.save()

                return Response({"message": "API Key set as primary successfully."}, status=200)

            else:
                # Handle invalid paths
                return Response({"error": "Invalid request path."}, status=400)

        except Exception as e:
            # Catch unexpected errors and return a 500 response
            return Response({"error": f"'POST' Method Failed for ApiKeyView: {str(e)}"}, status=500)
 
    def get(self, request):
        try:
            # Handle GET requests
           return Response({"message": "GET request received"}, status=200)
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for ApiKeyView: {e}"}, status=400)

    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for ApiKeyView: {e}"}, status=400)

    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for ApiKeyView: {e}"}, status=400)

    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for ApiKeyView: {e}"}, status=400)

    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for ApiKeyView: {e}"}, status=400)

    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for ApiKeyView: {e}"}, status=400)
