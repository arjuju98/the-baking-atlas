
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
# This creates a file called 'baking_atlas.db' in your backend folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./baking_atlas.db"

# Create the database engine
# check_same_thread=False is needed for SQLite to work with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create a SessionLocal class - this will be used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """
    Creates a database session for each request and closes it when done.
    
    Think of this like checking out a book from the library and returning it.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()