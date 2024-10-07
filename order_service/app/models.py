from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    address = db.Column(db.String(250),nullable=False)
    orders = db.relationship('Order', back_populates='user')
    type = db.Column(db.String(10), nullable=False, default='normal') 

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(400), nullable=True)
    price = db.Column(db.Float, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    orders = db.relationship('OrderProduct', back_populates='product')


class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order = db.relationship('Order', back_populates='products')
    product = db.relationship('Product', back_populates='orders')



class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    user = db.relationship('User', back_populates='orders')
    products = db.relationship('OrderProduct', back_populates='order')

    def add_product(self, product, quantity):
        order_product = OrderProduct(order=self, product=product, quantity=quantity)
        db.session.add(order_product)
    def to_dict(self):
        return {
        'id': self.id,
        'status': self.status,
        'user_id': self.user_id,
        'products': [
            {
                'product_id': order_product.product.id,
                'quantity': order_product.quantity
            } for order_product in self.products
        ]
    }