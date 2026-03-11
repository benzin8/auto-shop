from app.core.database import db

class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)