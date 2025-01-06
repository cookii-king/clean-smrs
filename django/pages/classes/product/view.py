from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from ...models import Product, Cart, CartItem
from ...serializers import ProductSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
class ProductView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        try:
            if request.path == '/product/create':
                serializer = ProductSerializer(data=request.data)
                if serializer.is_valid():
                    product = serializer.save()
                    product.create_or_get_stripe_product()  # Sync with Stripe
                    return redirect(f'/product/{product.id}')  # Redirect to the product detail page
                else:
                    return Response({"errors": serializer.errors}, status=400)

            elif request.path == '/product/edit':
                product_id = request.data.get("product_id")
                product = Product.objects.filter(id=product_id).first()
                if not product:
                    return Response({"error": "Product not found."}, status=404)

                serializer = ProductSerializer(product, data=request.data, partial=True)
                if serializer.is_valid():
                    updated_product = serializer.save()
                    updated_product.create_or_get_stripe_product()  # Sync updates with Stripe
                    return Response({"message": "Product updated successfully."}, status=200)
                else:
                    return Response({"errors": serializer.errors}, status=400)

            else:
                return Response({"error": "Unsupported path."}, status=404)

        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for ProductView: {e}"}, status=500)
    @method_decorator(login_required)
    def get(self, request, product_id=None):
        try:
            if request.path == '/product/create':
                return render(request, 'product/create.html')
            if request.path == '/product/edit':
                return render(request, 'product/edit.html')
            if product_id:  # Check if product_id is provided
                product = Product.objects.prefetch_related('images', 'prices').filter(id=product_id).first()
                if not product:
                    return Response({"error": "Product not found."}, status=404)
                return render(request, 'product/product.html', {"product": product})
            # Handle GET requests
            return render(request, 'product/product.html')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for ProductView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for ProductView: {e}"}, status=400)
    @method_decorator(login_required)
    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for ProductView: {e}"}, status=400)
    @method_decorator(login_required)
    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for ProductView: {e}"}, status=400)
    @method_decorator(login_required)
    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for ProductView: {e}"}, status=400)
    @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for ProductView: {e}"}, status=400)
    @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for ProductView: {e}"}, status=400)
    

class ProductsView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for ProductsView: {e}"}, status=400)
    @method_decorator(login_required)
    def get(self, request):
        try:
            # Handle GET requests
            # products = Product.objects.prefetch_related('images').all()
            products = Product.objects.filter(type='product', reoccurrence='one-time').prefetch_related('images', 'prices').all()
            return render(request, 'product/products.html', {"products": products})
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for ProductsView: {e}"}, status=400)
    @method_decorator(login_required)
    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for ProductsView: {e}"}, status=400)
    @method_decorator(login_required)
    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for ProductsView: {e}"}, status=400)
    @method_decorator(login_required)
    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for ProductsView: {e}"}, status=400)
    @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for ProductsView: {e}"}, status=400)
    @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for ProductsView: {e}"}, status=400)