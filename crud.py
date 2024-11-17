from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import update

# User CRUD
def create_user(db: Session, user: schemas.UserUpdate):
    db_user = models.User(username=user.username, password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        if user_update.username:
            db_user.username = user_update.username
        if user_update.password:
            db_user.password = user_update.password
        if user_update.role:
            db_user.role = user_update.role
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def deactivate_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.active = False  # Assuming there's an 'active' field to mark user as inactive
    db.commit()
    db.refresh(db_user)
    return db_user

# Customer CRUD
def create_customer(db: Session, customer: schemas.CustomerCreate):
    user = create_user(db, customer)  # Create the user
    db_customer = models.Customer(user_id=user.id, name=customer.name,
                                  delivery_address=customer.delivery_address,
                                  payment_details=customer.payment_details)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, user_id: int):
    return db.query(models.Customer).filter(models.Customer.user_id == user_id).first()

# Order CRUD
def get_orders(db: Session):
    return db.query(models.Order).all()

def manage_order(db: Session, order_id: int, status: str):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order

# Report CRUD
def get_most_popular_restaurants(db: Session):
    return db.query(models.RestaurantOwner.restaurant_name, db.func.count(models.Order.id).label("order_count")) \
        .join(models.Order, models.Order.restaurant_owner_id == models.RestaurantOwner.id) \
        .group_by(models.RestaurantOwner.id) \
        .order_by(db.func.count(models.Order.id).desc()).limit(5).all()

def get_average_delivery_time(db: Session):
    return db.query(db.func.avg(models.Delivery.delivery_time).label("avg_delivery_time")).scalar()

def get_order_trends(db: Session):
    return db.query(models.Order.status, db.func.count(models.Order.id).label("order_count")) \
        .group_by(models.Order.status).all()

# Menu CRUD
def create_menu(db: Session, menu: schemas.MenuBase):
    db_menu = models.Menu(restaurant_owner_id=menu.restaurant_owner_id, name=menu.name,
                          description=menu.description, price=menu.price, availability=menu.availability)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def update_menu(db: Session, menu_id: int, menu: schemas.MenuBase):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not db_menu:
        return None
    db_menu.name = menu.name
    db_menu.description = menu.description
    db_menu.price = menu.price
    db_menu.availability = menu.availability
    db.commit()
    db.refresh(db_menu)
    return db_menu

def delete_menu(db: Session, menu_id: int):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
    return db_menu
# Function to create a new delivery personnel
def create_delivery_personnel(db: Session, delivery_personnel: schemas.DeliveryPersonnelCreate):
    db_delivery_personnel = models.DeliveryPersonnel(
        name=delivery_personnel.name,
        contact_details=delivery_personnel.contact_details,
        vehicle_type=delivery_personnel.vehicle_type
    )
    db.add(db_delivery_personnel)
    db.commit()
    db.refresh(db_delivery_personnel)
    return db_delivery_personnel
def create_restaurant_owner(db: Session, restaurant_owner: schemas.RestaurantOwnerCreate):
    # Create a new user for the restaurant owner
    db_user = models.User(
        username=restaurant_owner.username,
        password=restaurant_owner.password,  # You should hash the password in production
        role="restaurant_owner"
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create a new restaurant owner linked to the user
    db_restaurant_owner = models.RestaurantOwner(
        user_id=db_user.id,
        restaurant_name=restaurant_owner.restaurant_name,
        address=restaurant_owner.address,
        hours_of_operation=restaurant_owner.hours_of_operation
    )
    
    db.add(db_restaurant_owner)
    db.commit()
    db.refresh(db_restaurant_owner)
    
    return db_restaurant_owner


# Function to create a new menu item
def create_menu_item(db: Session, menu: schemas.MenuCreate):
    # Create a new menu item
    db_menu = models.Menu(
        name=menu.name,
        description=menu.description,
        price=menu.price,
        availability=menu.availability
    )
    
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    
    return db_menu
# Function to generate a report based on report_type
def generate_report(report_type: str, db: Session):
    # Based on the report_type, query the database and return the data
    if report_type == "orders":
        # Example: Retrieve all orders
        return db.query(models.Order).all()  # You can customize this based on your needs
    elif report_type == "users":
        # Example: Retrieve all users
        return db.query(models.User).all()  # You can customize this based on your needs
    else:
        # Handle invalid report type
        return {"error": "Invalid report type"}
def generate_activity_report(db: Session):
    # Example data, this should be dynamically fetched based on your platform's actual data
    active_users = db.query(models.User).filter(models.User.is_active == True).count()
    total_deliveries = db.query(models.Delivery).count()
    orders_pending = db.query(models.Order).filter(models.Order.status == 'pending').count()
    orders_completed = db.query(models.Order).filter(models.Order.status == 'delivered').count()
    platform_uptime = "99.9%"  # This can be calculated based on uptime data if available

    return {
        'active_users': active_users,
        'total_deliveries': total_deliveries,
        'orders_pending': orders_pending,
        'orders_completed': orders_completed,
        'platform_uptime': platform_uptime
    }