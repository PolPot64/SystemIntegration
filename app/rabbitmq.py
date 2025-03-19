import pika
import json

RABBITMQ_HOST = "localhost"

def send_update(shipment_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue="shipment_updates")
    channel.queue_declare(queue="monitoring_tap")  # New queue for wiretap monitoring

    message = json.dumps(shipment_data)
    channel.basic_publish(exchange="", routing_key="shipment_updates", body=message)
    channel.basic_publish(exchange="", routing_key="monitoring_tap", body=message)  # Duplicate message

    print(f" [x] Sent {message}")
    connection.close()