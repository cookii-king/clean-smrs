from config.config import app, db
from classes.order_item import OrderItem, order_items_schema, order_item_schema
from flask import request, jsonify, abort

@app.post("/order-item/create")
def create_order_item():
    data = request.get_json()
    if not all(key in data for key in ("order_id", "price")):
        abort(400, description="Missing required fields: order_id, price")

    order_id = data["order_id"]
    price = data["price"]
    new_order_item = OrderItem.create(order_id, price)
    result = order_item_schema.dump(new_order_item)

    return jsonify(result), 201

@app.post("/order/<order_item_id>/delete")
def delete_order_item(order_item_id):
    order_item = OrderItem.soft_delete(order_item_id)
    if order_item:
        return {"message": f"Order item {order_item_id} soft deleted successfully.", "order_item": order_item_schema.dump(order_item)}, 200
    return {"message": "Order item not found."}, 404

@app.post("/order/<order_item_id>/delete-permanently")
def delete_order_item_permanently(order_item_id):
    result = OrderItem.delete(order_item_id)
    if "message" in result:
        return result, 200
    return {"message": "Order item not found."}, 404
