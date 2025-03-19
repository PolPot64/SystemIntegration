from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from .models import ShipmentEvent, Shipment, Base
from .crud import get_shipment_events, get_shipment, get_shipments, update_shipment
from .database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model matching your CRUD function
class ShipmentUpdate(BaseModel):
    status: str
    location: str

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get shipment events history
@app.get("/shipment_events")
def read_shipment_events(db: Session = Depends(get_db)):
    return get_shipment_events(db)

# Get single shipment details
@app.get("/shipments/{tracking_number}")
def read_shipment(tracking_number: str, db: Session = Depends(get_db)):
    shipment = get_shipment(db, tracking_number)
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

# Get all shipments
@app.get("/shipments/")
def read_all_shipments(db: Session = Depends(get_db)):
    return get_shipments(db)

# Updated endpoint clearly matching your CRUD function
@app.put("/shipments/{tracking_number}")
def update_shipment_endpoint(tracking_number: str, shipment_update: ShipmentUpdate, db: Session = Depends(get_db)):
    shipment = update_shipment(
        db,
        tracking_number=tracking_number,
        status=shipment_update.status,
        location=shipment_update.location
    )
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

# Static file serving clearly set
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../static")
app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")