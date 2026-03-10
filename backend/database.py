from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL. The file will be created in the project root.
DATABASE_URL = "sqlite:///./sql_app.db"

# Create a SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed for SQLite when using multiple threads (FastAPI workers)
# Otherwise, it raises an error when a session from one thread is used in another.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class to get a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def create_db_tables():
    """Creates all defined database tables. To be called on application startup."""
    # Import models here to ensure they are registered with Base.metadata
    from . import models
    Base.metadata.create_all(bind=engine)

