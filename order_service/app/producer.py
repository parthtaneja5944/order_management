import pika
import json

def order_created_event(order_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', pika.PlainCredentials('user', 'user')))
    channel = connection.channel()
    channel.queue_declare(queue='order_created')

    message = json.dumps(order_data)
    channel.basic_publish(exchange='', routing_key='order_created', body=message)
    print(f"Sent 'order_created' event: {message}")
    
    connection.close()
