from config.config import app, db
from classes.order import Order, orders_schema, order_schema
from flask import request, jsonify, abort

@app.put("/order/<order_id>/update")
def update_order(order_id):
    data = request.get_json()
    if not any(key in data for key in ("total_amount", "status")):
        abort(400, description="Missing required fields: total_amount or status")

    total_amount = data.get("total_amount")
    status = data.get("status")
    updated_order = Order.update(order_id, total_amount, status)

    if updated_order:
        result = order_schema.dump(updated_order)
        return jsonify(result), 200
    else:
        return {"message": "Order not found."}, 404