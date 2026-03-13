# Import required libraries
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from backend.database import create_connection

# Create the base class for our models
Base = declarative_base()

# Create a session maker to interact with the database
Session = sessionmaker(bind=create_connection())

# Define the user model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    first_name = Column(String(100))
    last_name = Column(String(100))
    age = Column(Integer)
    current_weight_kg = Column(Float)
    height_cm = Column(Float)
    activity_level = Column(Enum('sedentary', 'light', 'moderate', 'active', 'very_active'))
    desired_weight_kg = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Define the food item model
class FoodItem(Base):
    __tablename__ = 'food_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    brand = Column(String(255))
    calories_per_100g = Column(Float)
    protein_g_per_100g = Column(Float)
    carbs_g_per_100g = Column(Float)
    fat_g_per_100g = Column(Float)
    serving_size_g = Column(Float)
    serving_size_unit = Column(String(50))
    external_api_id = Column(String(255))
    is_custom = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Define the food log model
class FoodLog(Base):
    __tablename__ = 'food_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    food_item_id = Column(Integer, ForeignKey('food_items.id'))
    quantity_consumed = Column(Float)
    unit_consumed = Column(String(50))
    log_date = Column(DateTime)
    meal_type = Column(Enum('breakfast', 'lunch', 'dinner', 'snack', 'other'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Define the weight log model
class WeightLog(Base):
    __tablename__ = 'weight_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    weight_kg = Column(Float)
    log_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
