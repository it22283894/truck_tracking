from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

# Import our new database modules
import models
from database import engine, get_db

# 🏗️ Automatically generate the database tables if they don't exist yet
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Colombo Port Truck Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Updated data packet scheme to accept optional driver phone numbers
class TruckCheckIn(BaseModel):
    truck_id: str
    driver_phone: str = "" # Defaults to an empty string if not provided
    
@app.post("/api/checkin")
def check_in_truck(item: TruckCheckIn, db: Session = Depends(get_db)):
    # 1. Check if the truck is already sitting in the active queue
    existing_truck = db.query(models.TruckQueue).filter(models.TruckQueue.truck_id == item.truck_id).first()
    
    if existing_truck:
        return {
            "status": "exists",
            "message": f"Truck {item.truck_id} is already active in the queue.",
            "queue_position": existing_truck.id
        }
    
    # 2. If it's a new truck check-in, write it to the database ledger
    new_record = models.TruckQueue(
        truck_id=item.truck_id,
        driver_phone=item.driver_phone,
        status="QUEUED"
    )
    
    db.add(new_record)
    db.commit()      # Permanently write to disk!
    db.refresh(new_record)
    
    # 3. Calculate total trucks currently in front of them
    current_queue_count = db.query(models.TruckQueue).filter(models.TruckQueue.status == "QUEUED").count()

    return {
        "status": "success",
        "message": f"Truck {new_record.truck_id} safely stored in database ledger.",
        "queue_position": current_queue_count
    }

@app.get("/")
def home():
    return {"message": "Welcome to the Database-Connected Port Flow API!"}