# Import necessary libraries
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    daily_calorie_goals = Column(Integer, nullable=False)

# Define the FoodIntake model
class FoodIntake(Base):
    __tablename__ = 'food_intake'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    food_name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

# Define the FoodDatabase model
class FoodDatabase(Base):
    __tablename__ = 'food_database'

    id = Column(Integer, primary_key=True)
    food_name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
