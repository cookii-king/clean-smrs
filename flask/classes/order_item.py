import uuid
from config.config import db, ma
from datetime import datetime
from decimal import Decimal

class OrderItem(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(80), nullable=False)
    product_id = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return "<OrderItem %r>" % self.id

    @staticmethod
    def create(order_id, product_id, quantity, price):
        new_order_item = OrderItem(
            order_id=order_id,
            product_id= product_id,
            quantity= quantity,
            price= price,
        )
        db.session.add(new_order_item)
        db.session.commit()
        return new_order_item

    @staticmethod
    def get(order_item_id):
        order_item = OrderItem.query.get(order_item_id)
        return order_item

    @staticmethod
    def getAll():
        return OrderItem.query.all()
    
    @staticmethod
    def update(order_item_id, price=None, status=None):
        order_item = OrderItem.query.get(order_item_id)
        if order_item:
            if price is not None:
                order_item.price = Decimal(price)
            order_item.updated = datetime.utcnow()
            db.session.commit()
            return order_item
        return None
    
    @staticmethod
    def patch(order_item_id, price=None, status=None):
        order_item = OrderItem.query.get(order_item_id)
        if order_item:
            if price is not None:
                order_item.price = Decimal(price)
            order_item.updated = datetime.utcnow()
            db.session.commit()
            return order_item
        return None
    
    @staticmethod
    def soft_delete(order_item_id):
        order_item = OrderItem.query.get(order_item_id)
        if order_item:
            order_item.deleted = datetime.utcnow()
            db.session.commit()
            return order_item
        return None
    
    @staticmethod
    def delete(order_item_id):
        order_item = OrderItem.query.get(order_item_id)
        if order_item:
            db.session.delete(order_item)
            db.session.commit()
            return {"message": f"Order item {order_item_id} permanently deleted."}
        return {"message": "Order item not found."}
    


class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        fields = ("id", "order_id", "product_id", "quantity", "price", "created", "updated", "deleted")

order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)
