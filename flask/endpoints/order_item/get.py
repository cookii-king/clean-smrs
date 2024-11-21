from config.config import app, db
from classes.order_item import OrderItem, order_items_schema, order_item_schema
from flask import request, jsonify, abort

@app.get("/order-items")
def order_items():
    all_orders = OrderItem.getAll()
    result = order_items_schema.dump(all_orders)
    return jsonify(result)

@app.get("/order-item/<order_item_id>")
def order_item(order_item_id):
    order_item = OrderItem.get(order_item_id)
    if order_item is None:
        abort(404, description="Order item not found")
    result = order_item_schema.dump(order_item)
    return jsonify(result)