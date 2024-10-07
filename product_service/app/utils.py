from flask import jsonify
from app.models import db, Product, InventoryLog
from app.producer import product_created_event, product_updated_event
def create_product(data):
    name = data.get('name')
    description = data.get('description','')
    price = data.get('price')
    inventory = data.get('inventory')

    new_product = Product(name=name,description=description,price=price,inventory=inventory)

    db.session.add(new_product)
    db.session.commit()
    product_created_event(product=new_product)
    return new_product.to_dict()

def update_inventory(product, quantity):
    product.update_inventory(quantity)
    inventory_log = InventoryLog(product_id=product.id,inventory_change = -quantity)
    db.session.add(inventory_log)
    db.session.commit()
    product_updated_event(product=product)
