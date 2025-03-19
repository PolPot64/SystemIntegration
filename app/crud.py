from sqlalchemy.orm import Session
from .models import Shipment
from .models import ShipmentEvent
from .rabbitmq import send_update

# Create a new shipment
def create_shipment(db: Session, tracking_number: str, location: str):
    new_shipment = Shipment(tracking_number=tracking_number, location=location)
    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)
    return new_shipment

# Retrieve a shipment by tracking number
def get_shipment(db: Session, tracking_number: str):
    return db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()

# Retrieve all shipments
def get_shipments(db: Session):
    return db.query(Shipment).all()

# Retrieve all shipments events
def get_shipment_events(db: Session):
    return db.query(ShipmentEvent).order_by(ShipmentEvent.timestamp.desc()).all()

# Update shipment status and location
def update_shipment(db: Session, tracking_number: str, status: str, location: str):
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if shipment:
        # **Ensure this part exists:**
        shipment_event = ShipmentEvent(
            tracking_number=tracking_number,
            status=status,
            location=location
        )
        db.add(shipment_event)  # Add event to the database
        
        # Update latest shipment details
        shipment.status = status
        shipment.location = location
        db.commit()
        db.refresh(shipment)

        # Send update to RabbitMQ
        shipment_data = {"tracking_number": tracking_number, "status": status, "location": location}
        send_update(shipment_data)

    return shipment

# Delete a shipment
def delete_shipment(db: Session, tracking_number: str):
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if shipment:
        db.delete(shipment)
        db.commit()
    return shipment