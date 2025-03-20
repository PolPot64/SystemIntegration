import pika
import json

RABBITMQ_HOST = "localhost"

def process_shipment_update(body):
    """Process shipment update messages and log to terminal."""
    shipment_data = json.loads(body)

    print("\n📦 Shipment Update Received:")
    print(f"Tracking Number: {shipment_data.get('tracking_number', 'N/A')}")
    print(f"Status: {shipment_data.get('status', 'N/A')}")
    print(f"Location: {shipment_data.get('location', 'N/A')}")
    print(f"Timestamp: {shipment_data.get('timestamp', 'N/A')}")
    print("-" * 50)

def consume_updates():
    """Consume shipment updates from RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue="shipment_updates")

    def callback(ch, method, properties, body):
        process_shipment_update(body)

    channel.basic_consume(queue="shipment_updates", on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for shipment updates. To exit, press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    consume_updates()