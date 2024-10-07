import pika
import json

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', pika.PlainCredentials('user', 'user')))
    return connection

def send_event(event_name, user):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(queue='order_events')

    message = {
        'event': event_name,
        'user': user.to_dict()
    }

    channel.basic_publish(
        exchange='',
        routing_key='order_events',
        body=json.dumps(message)
    )

    connection.close()

def user_registered_event(user):
    print("user registerd event triggered")
    send_event(event_name='UserRegistered', user=user)

def user_updated_event(user):
    print("user update event triggered")
    send_event(event_name='UserUpdated', user=user)
