import pika
import json

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', pika.PlainCredentials('user', 'user')))
    return connection

def send_event(event_name,product):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare('order_events')

    message = {
        'event': event_name,
        'product': product.to_dict()
    }

    channel.basic_publish(
        exchange='',
        routing_key='order_events',
        body=json.dumps(message)
    )

    connection.close()

def product_created_event(product):
    send_event(event_name='ProductCreated',product=product)  

def product_updated_event(product):
    send_event(event_name='ProductUpdated',product=product)  

def product_deleted_event(product):
    send_event(event_name='ProductDeleted',product=product)  