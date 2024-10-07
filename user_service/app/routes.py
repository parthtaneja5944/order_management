from flask import Blueprint, request, jsonify
from .utils import register_user,login_user,get_user_profile,update_user,update_user_password, get_all_users, get_user_by_id
from flask_jwt_extended import jwt_required, get_jwt_identity

user_blueprint = Blueprint('user_blueprint',__name__)

@user_blueprint.route('/main')
def main():
    return "INVALID ROUTE"

@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    result = register_user(data)

    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result), 201

@user_blueprint.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    result = login_user(data)

    if "error" in result:
        return jsonify(result), 401
    
    return jsonify(access_token=result['access_token']), 200

@user_blueprint.route('/profile',methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()['id']
    user_info = get_user_profile(user_id)
    if 'error' in user_info:
        return jsonify(user_info), 400
    return jsonify(user_info), 200

@user_blueprint.route('/update', methods=['PUT'])
@jwt_required()
def update():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    result = update_user(user_id, data)

    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(message="User updated successfully"), 200

@user_blueprint.route('/update-password', methods=['PUT'])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()['id']  
    data = request.get_json()
    
    result = update_user_password(user_id, data)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(message="Password updated successfully"), 200

@user_blueprint.route('/all', methods=['GET'])
def get_users():
    users = get_all_users()  
    return jsonify(users), 200


@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)  
    if 'error' in user:
        return jsonify(user), 404  
    return jsonify(user), 200