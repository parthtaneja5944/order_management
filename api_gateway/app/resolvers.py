import requests
import jwt
from app.config import Config
from app.types import UserType , ProductType, ProductOrderType, OrderType

# USER_SERVICE_URL = "http://localhost:5001/users"
# PRODUCT_SERVICE_URL = "http://localhost:5002/products"
# ORDER_SERVICE_URL = "http://localhost:5003/orders"


USER_SERVICE_URL = "http://user_service:5000/users"
PRODUCT_SERVICE_URL = "http://product_service:5000/products"
ORDER_SERVICE_URL = "http://order_service:5000/orders"


def decode_jwt(token):
    try:
        payload = jwt.decode(token.split()[1], Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def resolve_user_profile(info):
    token = info.context.headers.get('Authorization')
    if not token:
        return {"error": "Authorization token is missing"}
    
    headers = {'Authorization': f'{token}'}
    response = requests.get(f"{USER_SERVICE_URL}/profile", headers=headers)
    print(response)
    if response.status_code == 200:
        user_data = response.json()
        return UserType(
            id=user_data.get('id'),
            username=user_data.get('username'),
            email=user_data.get('email'),
            address=user_data.get('address')
        )
    return {"error": "Unable to fetch user profile"}

def resolve_users(info):
    response = requests.get(f"{USER_SERVICE_URL}/all")
    if response.status_code == 200:
        users_data = response.json()
        users = [UserType(id=user["id"], username=user["username"], email=user["email"]) for user in users_data]

        return users
    return {"error": "Unable to fetch users"}

def resolve_user(user_id, info):
    response = requests.get(f"{USER_SERVICE_URL}/{user_id}")
    if response.status_code == 200:
        user_data = response.json()
        return UserType(
            id=user_data.get('id'),
            username=user_data.get('username'),
            email=user_data.get('email'),
            address=user_data.get('address')
        )
    return {"error": "Unable to fetch user"}

def register_user(input):
    response = requests.post(f"{USER_SERVICE_URL}/register", json=input)
    if response.status_code == 201:
        user_data = response.json()
        return UserType(
            id=user_data.get('id'),
            username=user_data.get('username'),
            email=user_data.get('email'),
            address=user_data.get('address')
        )
    return {"error": "Unable to fetch user"}

def login_user(input):
    response = requests.post(f"{USER_SERVICE_URL}/login", json=input)
    if response.status_code == 200:
        return response.json().get('access_token')
    return {"error": "Invalid login credentials"}


def resolve_products():
    response = requests.get(f"{PRODUCT_SERVICE_URL}")
    if response.status_code == 200:
        products_data = response.json().get("products", [])
        products = [ProductType(id=product["id"],name=product["name"], price=product["price"], inventory=product["inventory"], description=product["description"]) for product in products_data]

        return products
    return {"error": "Unable to fetch users"}

def resolve_product(product_id, info):
    token = info.context.headers.get('Authorization')
    if not token:
        return {"error": "Authorization token is missing"}
    
    payload = decode_jwt(token)
    if "error" in payload:
        return payload

    response = requests.get(f"{PRODUCT_SERVICE_URL}/{product_id}")

    if response.status_code == 200:
        product = response.json().get("product", [])
        return ProductType(id=product["id"],name=product["name"], price=product["price"], inventory=product["inventory"], description=product["description"])

    return {"error": "Unable to fetch users"}

def create_product(input, info):
    token = info.context.headers.get('Authorization')
    if not token:
        return {"error": "Authorization token is missing"}
    headers = {'Authorization': f'{token}'}
    payload = decode_jwt(token)
    if "error" in payload:
        return payload
    user_type = payload.get('sub', {}).get('type')
    if user_type != 'admin':
        return {"error": "Unauthorized: Only admins can create products"}
    response = requests.post(f"{PRODUCT_SERVICE_URL}/create", json=input, headers=headers)

    if response.status_code == 201:
        product_data = response.json()
        return ProductType(
            id =  product_data.get("id"),
            name = product_data.get("name"),
            price = product_data.get("price"),
            inventory = product_data.get("inventory"),
            description = product_data.get("description")
        )
    return {"error": "Failed to create product"}

def resolve_orders(info):
    token = info.context.headers.get('Authorization')
    print(token)
    if not token:
        return {"error": "Authorization token is missing"}
    payload = decode_jwt(token)
    print(payload)
    if "error" in payload:
        return payload
    user_id = payload.get('sub', {}).get('id')
    print(user_id)
    response = requests.get(f"{ORDER_SERVICE_URL}/user/{user_id}")
    if response.status_code == 200:
        orders_data = response.json().get("orders", [])
        orders = [
        OrderType(
            id=order['id'],
            user_id=order['user_id'],
            products=[
                ProductOrderType(product_id=product['product_id'], quantity=product['quantity'])
                for product in order['products']
            ]
        )
        for order in orders_data
    ]
        return orders
    return {"error": "Failed to fetch orders"}
    

def resolve_order(order_id):
    response = requests.get(f"{ORDER_SERVICE_URL}/order/{order_id}")

    if response.status_code != 200:
        return {"error": "Unable to fetch order"}

    order_data = response.json().get("order", {})
    order = OrderType(
        id=order_data['id'],
        user_id=order_data['user_id'],
        products=[
            ProductOrderType(product_id=product['product_id'], quantity=product['quantity'])
            for product in order_data.get('products', [])
        ]
    )

    return order


def place_order(input, info):
    token = info.context.headers.get('Authorization')
    if not token:
        return {"error": "Authorization token is missing"}

    payload = decode_jwt(token)
    if "error" in payload:
        return payload

    user_id = payload.get('sub', {}).get('id')
    order_data = {
        "user_id": user_id,
        "products": input.get("products")
    }
    response = requests.post(f"{ORDER_SERVICE_URL}/create_order", json=order_data)

    if response.status_code != 201:
        return {"error": "Order could not be created"}

    order_response = response.json()
    
    order_response = response.json()

    order_products = [
        ProductOrderType(product_id=product['product_id'], quantity=product['quantity'])
        for product in order_response.get("products", [])
    ]
    
    return OrderType(
        id=order_response.get("id"),
        user_id=order_response.get("user_id"),
        products=order_products
    )
