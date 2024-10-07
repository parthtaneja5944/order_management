from flask import Blueprint, jsonify, request
from app.utils import create_product, update_inventory
from app import db
from app.models import Product, InventoryLog
from app.producer import product_deleted_event
product_blueprint = Blueprint('product_blueprint',__name__)

@product_blueprint.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    try:
        product = create_product(data)
        return jsonify(product), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@product_blueprint.route('/<int:product_id>/update_inventory', methods=['PUT'])
def update(product_id):
    data = request.get_json()
    quantity = data.get('quantity')
    try:
        product = Product.query.get_or_404(product_id)
        update_inventory(product,quantity)
        return jsonify({"message":"Inventory updated successfully", "product_id":product_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@product_blueprint.route('/<int:product_id>', methods=['GET'])
def get_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error":"Product not found"}), 404
        
        return jsonify({"product" : product.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@product_blueprint.route('/<int:product_id>/delete', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        db.session.delete(product)
        db.session.commit()
        product_deleted_event(product=product)
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@product_blueprint.route('/', methods=['GET'])
def get_all_products():
    try:
        products = Product.query.all()
        return jsonify({"products": [product.to_dict() for product in products]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500