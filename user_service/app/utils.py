from flask import jsonify
from app.models import db, User
from flask_jwt_extended import create_access_token
from app.producer import user_registered_event,user_updated_event
from datetime import timedelta

def register_user(data):
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    address = data.get('address')
    type = data.get('type')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user is not None:
        return {"error":"User already exist"}
    
    user = User(username=username,email=email,address=address,type=type)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    user_registered_event(user)
    return user.to_dict()
   
def login_user(data):
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity={'id': user.id, 'type': user.type},expires_delta=timedelta(hours=1))
        return {"access_token": access_token}
    return {"error": "Invalid Credentials"}

def get_user_profile(user_id):
    user = User.query.filter_by(id = user_id).first()

    if user:
        return user.to_dict()
    return {"error": "no user found with given id"}

def update_user(user_id, data):
    user = User.query.get(user_id)
    
    if user is None:
        return {"error": "User not found"}

    username = data.get('username')
    email = data.get('email')
    address = data.get('address')
    type = data.get('type')
    if username:
        user.username = username
    if email:
        user.email = email
    if address:
        user.address = address
    if type:
        user.type = type    

    db.session.commit()

    user_updated_event(user)

    return {"id": user.id}
    

def update_user_password(user_id, data):
    new_password = data.get('new_password')
    old_password = data.get('old_password')

    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}

    if not user.check_password(old_password):
        return {"error": "Old password is incorrect"}

    user.set_password(new_password)
    db.session.commit()

    return {}

def get_all_users():
    try:
        users = User.query.all()  
        return [user.to_dict() for user in users]  
    except Exception as e:
        return {"error": str(e)}

def get_user_by_id(user_id):
    try:
        user_id = int(user_id)
        user = User.query.get(user_id)  
        print(user)
        if not user:
            return {"error": "User not found"}
        return user.to_dict() 
    except Exception as e:
        return {"error": str(e)}