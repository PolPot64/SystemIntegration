from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base
from pydantic import BaseModel

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True)
    status = Column(String, default="in_transit")
    location = Column(String)
    timestamp = Column(DateTime(timezone=True), default=func.now())

class ShipmentEvent(Base):
    __tablename__ = "shipment_events"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, index=True)
    status = Column(String)
    location = Column(String)
    timestamp = Column(DateTime(timezone=True), default=func.now())

class ShipmentUpdate(BaseModel):
    status: str
    location: str

class ShipmentLog(Base):
    __tablename__ = "shipment_logs"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, index=True)
    event_details = Column(String)
    timestamp = Column(DateTime(timezone=True), default=func.now())