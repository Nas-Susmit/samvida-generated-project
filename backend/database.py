# Import required libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a connection to the SQLite database
engine = create_engine('sqlite:///database.db')

# Create a base class for our models
Base = declarative_base()

# Create a session maker
Session = sessionmaker(bind=engine)

# Create all tables
Base.metadata.create_all(engine)
