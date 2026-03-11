from app.core.database import db

class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
       return f"<Brand {self.name}>"