from config.config import app, db
from classes.order_item import OrderItem, order_items_schema, order_item_schema
from flask import request, jsonify, abort

@app.patch("/order/order_item_id>/update")
def patch_order_item(order_item_id):
    data = request.get_json()
    price = data.get("price")

    updated_order_item = OrderItem.patch(order_item_id, price)

    if updated_order_item:
        result = order_item_schema.dump(updated_order_item)
        return jsonify(result), 200
    else:
        return {"message": "Order item not found."}, 404
