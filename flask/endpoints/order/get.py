from config.config import app, db
from classes.order import Order, orders_schema, order_schema
from flask import request, jsonify, abort

@app.get("/orders")
def orders():
    all_orders = Order.getAll()
    result = orders_schema.dump(all_orders)
    return jsonify(result)

@app.get("/order/<order_id>")
def order(order_id):
    order = Order.get(order_id)
    if order is None:
        abort(404, description="Order not found")
    result = order_schema.dump(order)
    return jsonify(result)