import pika
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import get_shipment, update_shipment
from ..models import ShipmentUpdate
from ..models import ShipmentEvent

router = APIRouter(prefix="/shipments", tags=["Shipments"])

def publish_update(message):
    """Send shipment update to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="shipment_updates")
    channel.basic_publish(exchange="", routing_key="shipment_updates", body=json.dumps(message))
    connection.close()

@router.put("/{tracking_number}")
def update_shipment_info(
        tracking_number: str,
        shipment_data: ShipmentUpdate,
        db: Session = Depends(get_db)
):
    shipment = get_shipment(db, tracking_number)
    if not shipment:
        raise HTTPException(status_code=404, detail="Tracking number not found")

    updated_shipment = update_shipment(db, tracking_number, shipment_data.status, shipment_data.location)

    # **Send update to RabbitMQ**
    message = {
        "tracking_number": tracking_number,
        "status": shipment_data.status,
        "location": shipment_data.location,
        "timestamp": str(updated_shipment.timestamp),
    }
    publish_update(message)

    return updated_shipment

@router.get("/events")
def get_all_shipment_events(db: Session = Depends(get_db)):
    events = db.query(ShipmentEvent).all()
    return events