import pika
import json
import asyncio
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect

RABBITMQ_HOST = "localhost"

# WebSocket manager for real-time updates
class WebSocketManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

ws_manager = WebSocketManager()

async def process_shipment_update(body):
    """Process shipment update messages."""
    shipment_data = json.loads(body)

    # Debugging Log
    print(f"📡 Broadcasting Update: {shipment_data}")

    # Ensure required fields exist
    if "tracking_number" not in shipment_data:
        print("❌ ERROR: Missing 'tracking_number' in shipment update!")
        return

    # Send the update once
    await ws_manager.broadcast(json.dumps(shipment_data))

def consume_updates():
    """Consume shipment updates from RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue="shipment_updates")

    def callback(ch, method, properties, body):
        asyncio.create_task(process_shipment_update(body))  # Non-blocking

    channel.basic_consume(queue="shipment_updates", on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for shipment updates. To exit, press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    consume_updates()