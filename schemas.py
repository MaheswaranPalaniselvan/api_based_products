from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True

class RestaurantBase(BaseModel):
    name: str
    address: str

class RestaurantCreate(RestaurantBase):
    owner_id: int

class Restaurant(RestaurantBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class MenuItemBase(BaseModel):
    name: str
    description: str
    price: float

class MenuItemCreate(MenuItemBase):
    restaurant_id: int

class MenuItem(MenuItemBase):
    id: int
    restaurant_id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_id: int
    restaurant_id: int
    status: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True
