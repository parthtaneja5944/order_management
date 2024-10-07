from app import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(400), nullable=True)
    price = db.Column(db.Float, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    inventory_logs = db.relationship('InventoryLog', backref='product', cascade="all, delete-orphan")

    def update_inventory(self, quantity):
        if self.inventory >= quantity:
            self.inventory -= quantity
        else:
            raise ValueError("Insufficient Inventory")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "inventory": self.inventory
        }    
        
class InventoryLog(db.Model):
    __tablename__ = 'inventory_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    inventory_change = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default = db.func.current_timestamp())        