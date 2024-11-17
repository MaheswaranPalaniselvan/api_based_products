from fastapi import FastAPI
from routers import customers, restaurant_owners, delivery_personnel, admins
from database import engine
import models
models.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app = FastAPI()

app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(restaurant_owners.router, prefix="/restaurant_owners", tags=["restaurant_owners"])
app.include_router(delivery_personnel.router, prefix="/delivery_personnel", tags=["delivery_personnel"])
app.include_router(admins.router, prefix="/admins", tags=["admins"])