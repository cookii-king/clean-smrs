from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ...serializers import ProductSerializer
from ...models import Product, Price

class ProductView(APIView):
    def post(self, request):
        try:
            # Check if the request path is for product creation
            if request.path == '/product/create':
                try:
                    serializer = ProductSerializer(data=request.data)
                    if serializer.is_valid():
                        product = serializer.save()
                        stripe_product = product.create_in_stripe()
                except Exception as e:
                    raise Exception(f"Failed to create product: {str(e)}") from e
            else:
                raise Exception("Invalid URL for POST request")
            # Return a success response
            return Response(data={"message": "Product created successfully!", "product_id": stripe_product["id"]}, status=201)
        except Exception as e:
            # Push the exception to the response
            return Response(data={"error": f"'POST' Method Failed for ProductView: {str(e)}"}, status=400)
    
    def get(self, request, product_id=None):
        try:
            account = request.user
            if request.path == '/product/create':
                return render(request, 'create-product.html', {'account': account})
            else:
                if product_id is None:  # Handle /product
                    raise Exception("Product not found")

                # Handle /product/<uuid:product_id>
                account = request.user
                try:
                    product = Product.objects.get(id=product_id)
                    prices = Price.objects.filter(product=product.stripe_product_id).all() 

                    # Add formatted price to each price object
                    for price in prices:
                        price.formatted_unit_amount = price.unit_amount / 100  # Divide by 100 to convert to pounds

                except Product.DoesNotExist as e:
                    raise Exception("Product not found") from e  # Chain exceptions
                
                return render(request, 'product.html', {'account': account, "product": product, 'prices': prices})
        except Exception as e:
            # Push the exception to the response
            return Response(data={"error": f"'GET' Method Failed for ProductView: {str(e)}"}, status=400)

class ProductsView(APIView):
    def post(self, request):
        try:
            return Response()
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for ProductsView: {e}"}, status=400)
    
    def get(self, request):
        try:
            account = request.user
            products = Product.objects.all()
            return render(request, 'products.html', {'account':account, "products": products})
        except Exception as e:
            return Response(data={"error": f"'GET' Method Failed for ProductsView: {e}"}, status=400)
