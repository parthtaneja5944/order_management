import pika
import json
from app import db, app 
from app.models import User, Product

def process_user_event(ch, method, properties, body):
    message = json.loads(body)  
    event = message['event']  
    if 'user' in message:
        user_data = message['user']
    if 'product' in message:
        product_data = message['product']

    
    with app.app_context():  
        if event == 'UserRegistered':
            print(f"Processing User Registered: {user_data}")
            new_user = User(id=user_data['id'], username=user_data['username'], email=user_data['email'], address=user_data['address'], type = user_data['type'])
            db.session.add(new_user)
            db.session.commit()

        elif event == 'UserUpdated':
            print(f"Processing User Updated: {user_data}")
            user = User.query.get(user_data['id'])
            if user:
                user.username = user_data['username']
                user.email = user_data['email']
                user.address = user_data['address']
                db.session.commit()
            else:
                print(f"User with ID {user_data['id']} not found.")
        elif event == 'ProductCreated':
            product_data = message['product']
            print(f" [x] Processing Product Created: {product_data}")
            new_product = Product(id=product_data['id'], name=product_data['name'], price=product_data['price'], inventory=product_data['inventory'])
            db.session.add(new_product)
            db.session.commit()

        elif event == 'ProductUpdated':
            product_data = message['product']
            print(f"Processing Product Updated: {product_data}")
            product = Product.query.get(product_data['id'])
            if product:
                product.name = product_data['name']
                product.price = product_data['price']
                product.inventory = product_data['inventory']
                db.session.commit()
            else:
                print(f"Product with ID {product_data['id']} not found.")

        elif event == 'ProductDeleted':
            product_data = message['product']
            print(f"Processing Product Deleted: {product_data}")
            product = Product.query.get(product_data['id'])
            if product:
                db.session.delete(product)
                db.session.commit()
            else:
                print(f"Product with ID {product_data['id']} not found.")        

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', pika.PlainCredentials('user', 'user')))
    channel = connection.channel()

    channel.queue_declare(queue='order_events')

    channel.basic_consume(queue='order_events', on_message_callback=process_user_event, auto_ack=True)

    print("Waiting for user events")
    channel.start_consuming()

if __name__ == "__main__":
    start_consuming()
