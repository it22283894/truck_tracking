import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class TruckQueue(Base):
    __tablename__ = "truck_queue"

    id = Column(Integer, primary_key=True, index=True)
    truck_id = Column(String, unique=True, index=True, nullable=False) # e.g., PI-09
    driver_phone = Column(String, nullable=True)                      # Driver contact
    status = Column(String, default="QUEUED")                         # QUEUED, INSPECTION, RELEASED
    check_in_time = Column(DateTime, default=datetime.datetime.utcnow) # Exact arrival time
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)