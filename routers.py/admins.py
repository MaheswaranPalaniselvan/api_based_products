from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, models
from database import get_db

router = APIRouter()

# Manage users (create, update, deactivate)
@router.post("/users/create")
def create_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db, user)

@router.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user_id, user)

@router.delete("/users/{user_id}")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.deactivate_user(db, user_id)

# View and manage all orders
@router.get("/orders", response_model=List[schemas.OrderBase])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders

@router.put("/orders/{order_id}")
def manage_order(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    db.refresh(order)
    return {"msg": f"Order {order_id} updated to {status}"}

# Generate reports
@router.get("/reports/{report_type}", response_model=schemas.Report)
def generate_report(report_type: str, db: Session = Depends(get_db)):
    if report_type == "popular_restaurants":
        data = crud.get_most_popular_restaurants(db)
    elif report_type == "average_delivery_time":
        data = crud.get_average_delivery_time(db)
    elif report_type == "order_trends":
        data = crud.get_order_trends(db)
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")
    return schemas.Report(report_type=report_type, data=data)

# Monitor platform activity
@router.get("/activity", response_model=schemas.ActivityReport)
def monitor_activity(db: Session = Depends(get_db)):
    active_users = db.query(models.User).filter(models.User.role != "admin").count()
    orders_in_progress = db.query(models.Order).filter(models.Order.status != "delivered").count()
    completed_orders = db.query(models.Order).filter(models.Order.status == "delivered").count()
    total_deliveries = db.query(models.Delivery).count()
    return schemas.ActivityReport(
        active_users=active_users,
        orders_in_progress=orders_in_progress,
        completed_orders=completed_orders,
        total_deliveries=total_deliveries
    )


# Endpoint to generate and get a report
@router.get("/reports/{report_type}", response_model=schemas.Report)
def get_report(report_type: str, db: Session = Depends(get_db)):
    # Call a function to generate the report data based on the report_type
    report_data = crud.generate_report(report_type, db)
    return schemas.Report(report_type=report_type, data=report_data)


# Endpoint to get the platform activity report
@router.get("/activity", response_model=schemas.ActivityReport)
def get_activity_report(db: Session = Depends(get_db)):
    # Call a function to generate the activity report
    activity_report = crud.generate_activity_report(db)
    return schemas.ActivityReport(
        active_users=activity_report['active_users'],
        total_deliveries=activity_report['total_deliveries'],
        orders_pending=activity_report['orders_pending'],
        orders_completed=activity_report['orders_completed'],
        platform_uptime=activity_report['platform_uptime']
    )