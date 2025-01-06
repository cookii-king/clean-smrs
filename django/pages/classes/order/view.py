from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from ...models import Order, Account
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
class OrderView(APIView): 
    @method_decorator(login_required)
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for OrderView: {e}"}, status=400)
    @method_decorator(login_required)
    def get(self, request):
        try:
            # Handle GET requests
            return render(request, 'order/order.html')
        except Exception as e:
            return render(request, 'system/response.html', {'message': f"'GET' Method Failed for OrderView: {e}", "is_error": True}, status=400)
                    # return Response(data={"error": f"'GET' Method Failed for OrderView: {e}"}, status=400)
    @method_decorator(login_required)
    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for OrderView: {e}"}, status=400)
    @method_decorator(login_required)
    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for OrderView: {e}"}, status=400)
    @method_decorator(login_required)
    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for OrderView: {e}"}, status=400)
    @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for OrderView: {e}"}, status=400)
    @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for OrderView: {e}"}, status=400)

class OrdersView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        try:
            # Handle POST requests
            return Response({"message": "POST request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'POST' Method Failed for OrdersView: {e}"}, status=400)
    @method_decorator(login_required)
    def get(self, request):
        try:
            user = request.user
            account = Account.objects.filter(id=user.id).first()
            # Fetch all orders for the user
            orders = Order.objects.filter(customer=account.stripe_customer_id).select_related(
                'customer'
            ).prefetch_related('order_items__product', 'order_items__price', 'order_items__plan')
            # Handle GET requests
            return render(request, 'order/orders.html', {"orders": orders})
        except Exception as e:
                    return Response(data={"error": f"'GET' Method Failed for OrdersView: {e}"}, status=400)
    @method_decorator(login_required)
    def put(self, request):
        try:
            # Handle PUT requests
            return Response({"message": "PUT request received"}, status=201)
        except Exception as e:
            return Response(data={"error": f"'PUT' Method Failed for OrdersView: {e}"}, status=400)
    @method_decorator(login_required)
    def patch(self, request):
        try:
            # Handle PATCH requests
            return Response({"message": "PATCH request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'PATCH' Method Failed for OrdersView: {e}"}, status=400)
    @method_decorator(login_required)
    def delete(self, request):
        try:
            # Handle DELETE requests
            return Response({"message": "DELETE request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'DELETE' Method Failed for OrdersView: {e}"}, status=400)
    @method_decorator(login_required)
    def options(self, request, *args, **kwargs):
        try:
            # Handle OPTIONS requests
            return Response({"message": "OPTIONS request received"}, status=204)
        except Exception as e:
            return Response(data={"error": f"'OPTIONS' Method Failed for OrdersView: {e}"}, status=400)
    @method_decorator(login_required)
    def head(self, request, *args, **kwargs):
        try:
            # Handle HEAD requests
            # Since Django automatically handles HEAD, no implementation is required
            # The HEAD response will be the same as GET but without the body
            return Response({"message": "HEAD request received"}, status=200)
        except Exception as e:
            return Response(data={"error": f"'HEAD' Method Failed for OrdersView: {e}"}, status=400)
