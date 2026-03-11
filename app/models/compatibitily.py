from app.core.database import db

class Compatibility(db.Model):
    __tablename__ = "compatibilities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)

    product = db.relationship('Product', backref='compatibilities')
    car = db.relationship('Car', backref='compatibilities')

    def __repr__(self):
        return f"<Compatibility Product ID: {self.product_id}, Car ID: {self.car_id}>"