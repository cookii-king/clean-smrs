from config.config import app, db
from classes.order import Order, orders_schema, order_schema
from flask import request, jsonify, abort

@app.post("/order/create")
def create_order():
    data = request.get_json()
    if not all(key in data for key in ("user_id", "total_amount", "status")):
        abort(400, description="Missing required fields: user_id, total_amount, and status")

    user_id = data["user_id"]
    total_amount = data["total_amount"]
    status = data["status"]
    new_order = Order.create(user_id, total_amount, status)
    result = order_schema.dump(new_order)

    return jsonify(result), 201

@app.post("/order/<order_id>/delete")
def delete_order(order_id):
    order = Order.soft_delete(order_id)
    if order:
        return {"message": f"Order {order_id} soft deleted successfully.", "order": order_schema.dump(order)}, 200
    return {"message": "Order not found."}, 404

@app.post("/order/<order_id>/delete-permanently")
def delete_order_permanently(order_id):
    result = Order.delete(order_id)
    if "message" in result:
        return result, 200
    return {"message": "Order not found."}, 404
