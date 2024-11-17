from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, models
from database import get_db

router = APIRouter()

# Register a new restaurant owner
@router.post("/register", response_model=schemas.RestaurantOwnerCreate)
def register_restaurant_owner(
    restaurant_owner: schemas.RestaurantOwnerCreate, 
    db: Session = Depends(get_db)
):
    # Call a CRUD function to create the restaurant owner in the database
    return crud.create_restaurant_owner(db, restaurant_owner)
# Login for restaurant owner
@router.post("/login")
def login_restaurant_owner(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"msg": "Login successful"}

# Manage Menus - Add, Update, or Remove Menu Items
@router.post("/menu", response_model=schemas.MenuBase)
def add_menu_item(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    # Add a menu item to the restaurant
    restaurant_owner = db.query(models.RestaurantOwner).filter(models.RestaurantOwner.user_id == menu.user_id).first()
    if not restaurant_owner:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    new_menu_item = crud.create_menu_item(db, menu, restaurant_owner.id)
    return new_menu_item

@router.put("/menu/{menu_id}", response_model=schemas.MenuBase)
def update_menu_item(menu_id: int, menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    # Update a specific menu item
    existing_menu_item = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not existing_menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    updated_menu_item = crud.update_menu_item(db, menu_id, menu)
    return updated_menu_item

@router.delete("/menu/{menu_id}")
def delete_menu_item(menu_id: int, db: Session = Depends(get_db)):
    # Delete a specific menu item
    menu_item = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    crud.delete_menu_item(db, menu_id)
    return {"msg": "Menu item deleted successfully"}

# View incoming orders for the restaurant owner
@router.get("/orders", response_model=List[schemas.OrderBase])
def view_orders(restaurant_owner_id: int, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.restaurant_owner_id == restaurant_owner_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders

# Update order status (e.g., order accepted, preparing, ready for delivery)
@router.put("/orders/{order_id}")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    db.refresh(order)
    return {"msg": "Order status updated", "status": order.status}

# Update restaurant details (e.g., hours of operation, address)
@router.put("/restaurant/{restaurant_owner_id}")
def update_restaurant_details(restaurant_owner_id: int, details: schemas.RestaurantOwnerCreate, db: Session = Depends(get_db)):
    restaurant_owner = db.query(models.RestaurantOwner).filter(models.RestaurantOwner.id == restaurant_owner_id).first()
    if not restaurant_owner:
        raise HTTPException(status_code=404, detail="Restaurant owner not found")
    restaurant_owner.restaurant_name = details.restaurant_name
    restaurant_owner.address = details.address
    restaurant_owner.hours_of_operation = details.hours_of_operation
    db.commit()
    db.refresh(restaurant_owner)
    return {"msg": "Restaurant details updated", "restaurant_name": restaurant_owner.restaurant_name}


# Endpoint to add a new menu item
@router.post("/add_menu_item", response_model=schemas.MenuCreate)
def add_menu_item(
    menu: schemas.MenuCreate, 
    db: Session = Depends(get_db)
):
    # Call a CRUD function to add the menu item to the database
    return crud.create_menu_item(db, menu)