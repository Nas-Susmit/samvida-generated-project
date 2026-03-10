# SQLAlchemy Models
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    daily_calorie_goal = Column(Integer)

class FoodIntake(Base):
    __tablename__ = 'food_intake'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    food_name = Column(String)
    calories = Column(Integer)
    date = Column(Date)

class PhysicalActivity(Base):
    __tablename__ = 'physical_activity'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    activity_name = Column(String)
    calories_burned = Column(Integer)
    date = Column(Date)

class FoodDatabase(Base):
    __tablename__ = 'food_database'
    id = Column(Integer, primary_key=True)
    food_name = Column(String)
    calories = Column(Integer)
