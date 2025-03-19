import pika
import json
from .database import SessionLocal
from .models import ShipmentLog

RABBITMQ_HOST = "localhost"

def log_event(tracking_number, event_details):
    db = SessionLocal()
    new_log = ShipmentLog(tracking_number=tracking_number, event_details=event_details)
    db.add(new_log)
    db.commit()
    db.close()

def consume_monitoring():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue="monitoring_tap")

    def callback(ch, method, properties, body):
        shipment_data = json.loads(body)
        tracking_number = shipment_data.get("tracking_number")
        event_details = f"Status: {shipment_data.get('status')} | Location: {shipment_data.get('location')}"
        
        print(f" [MONITOR] Logging Event: {event_details}")  # Debugging
        log_event(tracking_number, event_details)

    channel.basic_consume(queue="monitoring_tap", on_message_callback=callback, auto_ack=True)
    print(" [*] Monitoring shipment updates. Press CTRL+C to exit.")
    channel.start_consuming()

if __name__ == "__main__":
    consume_monitoring()