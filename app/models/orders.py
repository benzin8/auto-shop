from app.core.database import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    status = db.Column(db.String(50), nullable=False, default='pending')
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    items = db.relationship('OrderComposition', backref='order', lazy=True)


class OrderComposition(db.Model):
    __tablename__ = "order_composition"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_order = db.Column(db.Numeric(10, 2), nullable=False)

    product = db.relationship('Product', backref='order_compositions')
    