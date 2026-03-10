# Import necessary libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a database engine
engine = create_engine('sqlite:///database.db')

# Create a session maker
Session = sessionmaker(bind=engine)
