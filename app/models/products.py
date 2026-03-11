from app.core.database import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)

    brand = db.relationship('Brand', backref='products')
    category = db.relationship('Category', backref='products')
    car = db.relationship('Car', secondary='compatibilities', backref='products')

    def __repr__(self):
        return f"<Product {self.name} (SKU: {self.sku})>"

