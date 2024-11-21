from config.config import app, db
from classes.order_item import OrderItem, order_items_schema, order_item_schema
from flask import request, jsonify, abort

@app.put("/order-item/<order_item_id>/update")
def update_order_item(order_item_id):
    data = request.get_json()
    if not any(key in data for key in ("price")):
        abort(400, description="Missing required fields: price")

    price = data.get("price")
    updated_order_item = OrderItem.update(order_item_id, price)

    if updated_order_item:
        result = order_item_schema.dump(updated_order_item)
        return jsonify(result), 200
    else:
        return {"message": "Order item not found."}, 404