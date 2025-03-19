from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import create_shipment, get_shipment, get_shipments, update_shipment, delete_shipment
from ..models import ShipmentUpdate
from ..models import ShipmentEvent
from ..models import ShipmentLog

router = APIRouter(prefix="/shipments", tags=["Shipments"])

# Create a new shipment
@router.post("/")
def add_shipment(tracking_number: str, location: str, db: Session = Depends(get_db)):
    return create_shipment(db, tracking_number, location)

# Get all shipments
@router.get("/")
def list_shipments(db: Session = Depends(get_db)):
    return get_shipments(db)

# Get a shipment by tracking number
@router.get("/{tracking_number}")
def get_shipment_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    shipment = get_shipment(db, tracking_number)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

# Get a shipment's history
@router.get("/{tracking_number}/history")
def get_shipment_history(tracking_number: str, db: Session = Depends(get_db)):
    history = db.query(ShipmentEvent).filter(ShipmentEvent.tracking_number == tracking_number).all()
    if not history:
        raise HTTPException(status_code=404, detail="No history found for this shipment")
    return history

# Get a shipment's logs
@router.get("/{tracking_number}/logs")
def get_shipment_logs(tracking_number: str, db: Session = Depends(get_db)):
    logs = db.query(ShipmentLog).filter(ShipmentLog.tracking_number == tracking_number).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this shipment")
    return logs

# Update a shipment
@router.put("/{tracking_number}")
def update_shipment_info(
        tracking_number: str,
        shipment_data: ShipmentUpdate,  # Accept JSON body
        db: Session = Depends(get_db)
):
    if not get_shipment(db, tracking_number):
        raise HTTPException(status_code=404, detail="Tracking number not found")
    return update_shipment(db, tracking_number, shipment_data.status, shipment_data.location)

# Delete a shipment
@router.delete("/{tracking_number}")
def remove_shipment(tracking_number: str, db: Session = Depends(get_db)):
    shipment = delete_shipment(db, tracking_number)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return {"message": "Shipment deleted"}