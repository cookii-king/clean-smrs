import uuid
from config.config import db, ma
from datetime import datetime
from decimal import Decimal

class Order(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(80), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return "<Order %r>" % self.id

    @staticmethod
    def create(user_id, total_amount, status):
        new_order = Order(
            user_id=user_id,
            order_date=datetime.utcnow(),
            total_amount=Decimal(total_amount),
            status=status,
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order

    @staticmethod
    def get(order_id):
        order = Order.query.get(order_id)
        return order

    @staticmethod
    def getAll():
        return Order.query.all()
    
    @staticmethod
    def update(order_id, total_amount=None, status=None):
        order = Order.query.get(order_id)
        if order:
            if total_amount is not None:
                order.total_amount = Decimal(total_amount)
            if status is not None:
                order.status = status
            order.updated = datetime.utcnow()
            db.session.commit()
            return order
        return None
    
    @staticmethod
    def patch(order_id, total_amount=None, status=None):
        order = Order.query.get(order_id)
        if order:
            if total_amount is not None:
                order.total_amount = Decimal(total_amount)
            if status is not None:
                order.status = status
            order.updated = datetime.utcnow()
            db.session.commit()
            return order
        return None
    
    @staticmethod
    def soft_delete(order_id):
        order = Order.query.get(order_id)
        if order:
            order.deleted = datetime.utcnow()
            db.session.commit()
            return order
        return None
    
    @staticmethod
    def delete(order_id):
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return {"message": f"Order {order_id} permanently deleted."}
        return {"message": "Order not found."}
    


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        fields = ("id", "user_id", "order_date", "total_amount", "status", "created", "updated", "deleted")

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
