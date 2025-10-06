from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Product {self.product_id}>"

class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Location {self.location_id}>"

class ProductMovement(db.Model):
    __tablename__ = 'product_movements'
    movement_id = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    from_location = db.Column(db.String, db.ForeignKey('locations.location_id'), nullable=True)
    to_location = db.Column(db.String, db.ForeignKey('locations.location_id'), nullable=True)
    product_id = db.Column(db.String, db.ForeignKey('products.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Movement {self.movement_id} {self.product_id} {self.qty}>"
