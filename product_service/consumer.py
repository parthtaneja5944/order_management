import pika
import json
from app import db, app
from app.models import Product

def update_inventory(product_id, quantity):
    product = Product.query.get(product_id)
    if product:
        product.inventory -= quantity
        db.session.commit()

def process_order_event(ch, method, properties, body):
    data = json.loads(body)
    products = data.get('products')

    with app.app_context():
        for item in products:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            update_inventory(product_id, quantity)

        print(f"Processed 'order_created' event for Order ID: {data.get('order_id')}")

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', pika.PlainCredentials('user', 'user')))
    channel = connection.channel()
    channel.queue_declare(queue='order_created')

    channel.basic_consume(queue='order_created', on_message_callback=process_order_event,auto_ack=True)

    print('Waiting for order_created events...')
    channel.start_consuming()

if __name__ == '__main__':
    start_consuming()
