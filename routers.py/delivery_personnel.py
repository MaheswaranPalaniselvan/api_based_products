from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, models
from database import get_db

router = APIRouter()

# Register a new delivery personnel
@router.post("/register")
def register_delivery_personnel(delivery_personnel: schemas.DeliveryPersonnelCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, delivery_personnel)
    return crud.create_delivery_personnel(db, delivery_personnel, user.id)

# Login for delivery personnel
@router.post("/login")
def login_delivery_personnel(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"msg": "Login successful"}

# View available deliveries for delivery personnel
@router.get("/deliveries", response_model=List[schemas.DeliveryBase])
def view_available_deliveries(db: Session = Depends(get_db), delivery_personnel_id: int = None):
    deliveries = db.query(models.Delivery).filter(models.Delivery.delivery_personnel_id == delivery_personnel_id, models.Delivery.status == "available").all()
    if not deliveries:
        raise HTTPException(status_code=404, detail="No available deliveries found")
    return deliveries

# Accept a delivery
@router.put("/deliveries/{delivery_id}")
def accept_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not delivery or delivery.status != "available":
        raise HTTPException(status_code=404, detail="Delivery not available")
    delivery.status = "picked up"
    db.commit()
    db.refresh(delivery)
    return {"msg": "Delivery accepted", "status": delivery.status}

# Track delivery status (e.g., picked up, en route, delivered)
@router.put("/deliveries/status/{delivery_id}")
def update_delivery_status(delivery_id: int, status: str, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    delivery.status = status
    db.commit()
    db.refresh(delivery)
    return {"msg": "Delivery status updated", "status": delivery.status}

# Manage delivery availability (set availability for delivery personnel)
@router.put("/availability/{delivery_personnel_id}")
def set_delivery_availability(delivery_personnel_id: int, availability: schemas.DeliveryAvailability, db: Session = Depends(get_db)):
    delivery_personnel = db.query(models.DeliveryPersonnel).filter(models.DeliveryPersonnel.id == delivery_personnel_id).first()
    if not delivery_personnel:
        raise HTTPException(status_code=404, detail="Delivery personnel not found")
    # Here, we can toggle availability flag based on the provided data
    # Assuming `availability` is a boolean, we will store it as such
    delivery_personnel.available = availability.available
    db.commit()
    db.refresh(delivery_personnel)
    return {"msg": "Availability updated", "available": delivery_personnel.available}