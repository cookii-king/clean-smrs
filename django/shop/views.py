from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrderSerializer
from .models import Order

class OrderView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."})
     # POST method to create a new order
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new order to the database
            return Response(serializer.data)
        return Response(serializer.errors)
    

class OrdersView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

