from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 📍 Local SQLite database URL for development
# (We use SQLite locally because it runs out of a simple file without needing server installs)
SQLALCHEMY_DATABASE_URL = "sqlite:///./port_logistics.db"

# Create the database engine
engine = create_engine(
    # check_same_thread=False is only needed for SQLite, not PostgreSQL
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class - each instance will be a distinct database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our database models will inherit from
Base = declarative_base()

# Dependency helper to get a database session for our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()