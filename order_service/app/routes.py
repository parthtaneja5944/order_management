from flask import Blueprint, jsonify, request
from app import db
from app.models import Order, OrderProduct, User, Product
from app.producer import order_created_event
order_blueprint = Blueprint('order_blueprint',__name__)

@order_blueprint.route('/create_order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        print(data)
        user_id = data.get('user_id')
        products = data.get('products')

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        print(user)
        order = Order(user_id=user.id)
        product_list = []
        print(order)
        for product_data in products:
            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity')  
            
            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": f"Product {product_id} not found"}), 404

            if product.inventory < quantity:
                return jsonify({"error": f"Insufficient inventory for product {product.name}"}), 400
            
            product.inventory -= quantity
            order.add_product(product, quantity)

            product_list.append({
                'product_id': product_id,
                'quantity': quantity
            })
        print(order)
        db.session.add(order)
        db.session.commit()

        order_created_event({
            'order_id': order.id,
            'user_id': user_id,
            'products': product_list
        })
        return jsonify(order.to_dict()), 201
        return jsonify({"message": "Order placed successfully", "order_id": order.id}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@order_blueprint.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        order_data = {
            "id": order.id,
            "user_id": order.user_id,
                "products": [
                    {
                        "product_id": op.product.id,
                        "quantity": op.quantity,
                    }
                    for op in order.products
                ]
        }
        return jsonify({"order": order_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@order_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        orders = Order.query.filter_by(user_id=user.id).all()
        order_list = []
        for order in orders:
            order_data = {
                "id": order.id,
                "user_id": order.user_id,
                "products": [
                    {
                        "product_id": op.product.id,
                        "quantity": op.quantity,
                    }
                    for op in order.products
                ]
            }
            order_list.append(order_data)

        return jsonify({"orders": order_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    