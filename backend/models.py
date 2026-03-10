# Import required libraries
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from backend.database import Base

# Define the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    daily_calorie_goals = Column(Integer)

# Define the Food model
class Food(Base):
    __tablename__ = 'foods'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    calories = Column(Integer)
