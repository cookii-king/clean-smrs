from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ...serializers import PriceSerializer
from ...models import Price

class PriceView(APIView):
    def post(self, request):
        try:
            # Check if the request path is for price creation
            if request.path == '/price/create':
                try:
                    data = request.data.dict()

                    recurring_data = {}
                    interval = data.pop('recurring[interval]', None)
                    aggregate_usage = data.pop('recurring[aggregate_usage]', None)

                    if interval:
                        recurring_data['interval'] = interval
                    if aggregate_usage:
                        recurring_data['aggregate_usage'] = aggregate_usage

                    if recurring_data:
                        data['recurring'] = recurring_data

                    print(f"Constructed data: {data}")
                    serializer = PriceSerializer(data=data)
                    if serializer.is_valid():
                        price = serializer.save()
                        stripe_price = price.create_in_stripe()
                except Exception as e:
                    raise Exception(f"Failed to create price: {str(e)}") from e
            else:
                raise Exception("Invalid URL for POST request")
            # Return a success response
            return Response(data={"message": "Price created successfully!", "price_id": stripe_price["id"]}, status=201)
        except Exception as e:
            # Push the exception to the response
            return Response(data={"error": f"'POST' Method Failed for PriceView: {str(e)}"}, status=400)
    
    def get(self, request, price_id=None):
        try:
            account = request.user
            if request.path == '/price/create':
                return render(request, 'create-price.html', {'account': account})
            else:
                if price_id is None:  # Handle /price
                    raise Exception("Price not found")

                # Handle /price/<uuid:price_id>
                account = request.user
                try:
                    price = Price.objects.get(id=price_id)
                except Price.DoesNotExist as e:
                    raise Exception("Price not found") from e  # Chain exceptions
                
                return render(request, 'price.html', {'account': account, "price": price})
        except Exception as e:
            # Push the exception to the response
            return Response(data={"error": f"'GET' Method Failed for PriceView: {str(e)}"}, status=400)

class PricesView(APIView):
    def post(self, request):
        try:
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for PricesView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            prices = Price.objects.all()
            return render(request, 'prices.html', {'account':account, "prices": prices})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for PricesView: {e}"}, status=400)
