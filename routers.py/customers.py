from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, models
from database import get_db

router = APIRouter()

# Register a new customer
@router.post("/register")
def register_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    user = crud.create_user(db, customer)
    return crud.create_customer(db, customer, user.id)

# Login an existing customer
@router.post("/login")
def login_customer(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"msg": "Login successful"}

# Browse Restaurants - List all restaurants
@router.get("/restaurants", response_model=List[schemas.RestaurantOwnerBase])
def browse_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(models.RestaurantOwner).all()
    return restaurants

# View Menu of a particular restaurant
@router.get("/restaurants/{restaurant_id}/menu", response_model=List[schemas.MenuBase])
def view_menu(restaurant_id: int, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.restaurant_owner_id == restaurant_id).all()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu

# Search menus by item name, cuisine, or vegetarian options
@router.get("/search-menu")
def search_menu(query: str, db: Session = Depends(get_db)):
    results = db.query(models.Menu).filter(models.Menu.name.ilike(f"%{query}%")).all()
    if not results:
        raise HTTPException(status_code=404, detail="No items found")
    return results

# Place an order
@router.post("/order")
def place_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Validate the order (e.g., check menu item availability, customer, and restaurant existence)
    db_order = crud.create_order(db, order)
    return {"msg": "Order placed successfully", "order_id": db_order.id}

# Track an order
@router.get("/order/{order_id}")
def track_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order.id, "status": order.status}

# View past orders and reorder
@router.get("/order-history", response_model=List[schemas.OrderBase])
def view_order_history(customer_id: int, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No past orders found")
    return orders

# Reorder from the same restaurant
@router.post("/reorder/{order_id}")
def reorder(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Create a new order based on the previous order details
    new_order = schemas.OrderCreate(
        customer_id=order.customer_id,
        restaurant_owner_id=order.restaurant_owner_id,
        status="pending",
        total_amount=order.total_amount
    )
    db_order = crud.create_order(db, new_order)
    return {"msg": "Order reordered successfully", "order_id": db_order.id}