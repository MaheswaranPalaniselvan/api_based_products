from pydantic import BaseModel
from typing import List, Optional
# Update schema for User
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None  # 'customer', 'restaurant_owner', 'delivery_personnel'

# 1. Customer Schemas
class CustomerBase(BaseModel):
    username: str
    password: str
    name: str
    delivery_address: str
    payment_details: str

class CustomerProfile(CustomerBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class CustomerOrderHistory(BaseModel):
    order_id: int
    status: str
    total_amount: int

    class Config:
        orm_mode = True

# Customer Create Schema
class CustomerCreate(BaseModel):
    name: str
    delivery_address: str
    payment_details: str

    class Config:
        orm_mode = True

# Customer Response Schema
class CustomerResponse(BaseModel):
    id: int
    name: str
    delivery_address: str
    payment_details: str

    class Config:
        orm_mode = True
# 2. Restaurant Owner Schemas
class RestaurantOwnerBase(BaseModel):
    username: str
    password: str
    restaurant_name: str
    address: str
    hours_of_operation: str

class RestaurantOwnerProfile(RestaurantOwnerBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class RestaurantMenu(BaseModel):
    id: int
    name: str
    description: str
    price: int
    availability: bool

    class Config:
        orm_mode = True

class RestaurantOrder(BaseModel):
    order_id: int
    customer_id: int
    status: str
    total_amount: int

    class Config:
        orm_mode = True

# 3. Delivery Personnel Schemas
class DeliveryPersonnelBase(BaseModel):
    username: str
    password: str
    name: str
    contact_details: str
    vehicle_type: str

class DeliveryPersonnelProfile(DeliveryPersonnelBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class DeliveryAssignment(BaseModel):
    order_id: int
    status: str  # E.g., "picked up", "en route", "delivered"

    class Config:
        orm_mode = True

# DeliveryBase Schema - Represents the basic details of a delivery
class DeliveryBase(BaseModel):
    order_id: int
    delivery_personnel_id: int
    status: str  # e.g., "picked up", "en route", "delivered"
    delivery_time: Optional[str] = None  # Time when delivery occurred, optional

    class Config:
        orm_mode = True

# Delivery Response Schema - Includes additional fields
class DeliveryResponse(DeliveryBase):
    id: int
    delivery_personnel_name: str
    order_status: str

    class Config:
        orm_mode = True

# Delivery Personnel Create Schema
class DeliveryPersonnelCreate(BaseModel):
    name: str
    contact_details: str
    vehicle_type: str

    class Config:
        orm_mode = True

# Delivery Personnel Response Schema (for returning delivery personnel data)
class DeliveryPersonnelResponse(DeliveryPersonnelCreate):
    id: int

    class Config:
        orm_mode = True
# 4. Admin Schemas
class AdminBase(BaseModel):
    username: str
    password: str

class AdminProfile(AdminBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserManagement(BaseModel):
    user_id: int
    role: str  # 'customer', 'restaurant_owner', 'delivery_personnel'
    status: str  # 'active', 'inactive'

    class Config:
        orm_mode = True

class OrderManagement(BaseModel):
    order_id: int
    customer_id: int
    status: str  # 'pending', 'canceled', 'completed'

    class Config:
        orm_mode = True

# 5. Order and Menu Schemas
# Order Schema
class OrderBase(BaseModel):
    customer_id: int
    restaurant_owner_id: int
    status: str  # 'preparing', 'out for delivery', 'delivered'
    total_amount: int

class OrderCreate(OrderBase):
    items: List[int]  # List of menu items

class OrderUpdate(BaseModel):
    status: str  # Update order status

class OrderResponse(OrderBase):
    id: int
    customer: str
    restaurant_owner: str

    class Config:
        orm_mode = True

# Menu Item Schema
class MenuItemBase(BaseModel):
    name: str
    description: str
    price: int
    availability: bool

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    availability: Optional[bool]

class MenuItemResponse(MenuItemBase):
    id: int
    restaurant_owner_id: int

    class Config:
        orm_mode = True


# Menu Base Schema (for creating or updating menu)
class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    availability: bool = True

    class Config:
        orm_mode = True

# Menu Response Schema (for returning menu data)
class MenuResponse(MenuBase):
    id: int

    class Config:
        orm_mode = True
# 6. JWT Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: str  # 'customer', 'restaurant_owner', 'delivery_personnel'
# Schema for updating the availability of delivery personnel
class DeliveryAvailability(BaseModel):
    available: bool  # Whether the delivery personnel is available for deliveries

    class Config:
        orm_mode = True
# Schema for creating a new restaurant owner
class RestaurantOwnerCreate(BaseModel):
    username: str  # Username for the restaurant owner account
    password: str  # Password for the restaurant owner account
    restaurant_name: str  # Name of the restaurant
    address: str  # Address of the restaurant
    hours_of_operation: str  # Operating hours of the restaurant

    class Config:
        orm_mode = True
# Schema for creating a new menu
class MenuCreate(BaseModel):
    name: str  # Name of the menu
    description: str  # Description of the menu
    price: float  # Price of the menu item
    availability: bool  # Whether the menu item is available

    class Config:
        orm_mode = True
# Schema for generating reports
class Report(BaseModel):
    report_type: str  # Type of the report (e.g., "orders", "users")
    data: List[dict]  # Data in the report, can be a list of dictionaries or any structured format you choose

    class Config:
        orm_mode = True


# Schema for platform activity report
class ActivityReport(BaseModel):
    active_users: int  # Number of active users
    total_deliveries: int  # Total number of deliveries
    orders_pending: int  # Number of orders pending
    orders_completed: int  # Number of completed orders
    platform_uptime: str  # Uptime status or a timestamp

    class Config:
        orm_mode = True