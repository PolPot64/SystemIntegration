from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://logistics_user:password@localhost/logistics_tracking"

# Create Database Engine
engine = create_engine(DATABASE_URL)

# Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency: Get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
