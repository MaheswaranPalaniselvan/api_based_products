import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


with open('config.json') as config_file:
    config = json.load(config_file)

DATABASE_URL = f"mysql+pymysql://{config['database']['username']}:{config['database']['password']}@{config['database']['host']}/{config['database']['database']}"



# Create database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()