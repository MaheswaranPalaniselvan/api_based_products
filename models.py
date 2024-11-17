from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(255))  # 'customer', 'restaurant_owner', 'delivery_personnel', 'admin'
    active = Column(Boolean, default=True)  # Mark as active or deactivated

    # Relationships
    customer = relationship("Customer", back_populates="user", uselist=False)
    restaurant_owner = relationship("RestaurantOwner", back_populates="user", uselist=False)
    delivery_personnel = relationship("DeliveryPersonnel", back_populates="user", uselist=False)

# Customer Model
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    delivery_address = Column(String(255))
    payment_details = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    user = relationship("User", back_populates="customer")
    orders = relationship("Order", back_populates="customer")

# Order Model
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    restaurant_owner_id = Column(Integer, ForeignKey("restaurant_owners.id"))
    status = Column(String(50))  # e.g., "preparing", "out for delivery", "delivered"
    total_amount = Column(Integer)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    restaurant_owner = relationship("RestaurantOwner", back_populates="orders")
    delivery = relationship("Delivery", back_populates="order", uselist=False)

# Restaurant Owner Model
class RestaurantOwner(Base):
    __tablename__ = 'restaurant_owners'

    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(255))
    address = Column(String(255))
    hours_of_operation = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    user = relationship("User", back_populates="restaurant_owner")
    menus = relationship("Menu", back_populates="restaurant_owner")
    orders = relationship("Order", back_populates="restaurant_owner")

# Menu Model
class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True)
    restaurant_owner_id = Column(Integer, ForeignKey("restaurant_owners.id"))
    name = Column(String(255))
    description = Column(String(255))
    price = Column(Integer)
    availability = Column(Boolean, default=True)

    # Relationships
    restaurant_owner = relationship("RestaurantOwner", back_populates="menus")

# Delivery Model
class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    delivery_personnel_id = Column(Integer, ForeignKey("delivery_personnel.id"))
    status = Column(String(50))  # e.g., "picked up", "en route", "delivered"
    delivery_time = Column(Integer)

    # Relationships
    order = relationship("Order", back_populates="delivery")
    delivery_personnel = relationship("DeliveryPersonnel", back_populates="deliveries")

# Delivery Personnel Model
class DeliveryPersonnel(Base):
    __tablename__ = 'delivery_personnel'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    contact_details = Column(String(255))
    vehicle_type = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_available = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="delivery_personnel")
    deliveries = relationship("Delivery", back_populates="delivery_personnel")