# FastAPI Routes
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import User, FoodIntake, PhysicalActivity, FoodDatabase
from database import get_db
from typing import List

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

class UserRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login_user(user: UserRequest):
    # Login logic here
    pass

@router.post("/register")
def register_user(user: UserRequest):
    # Register logic here
    pass

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/food_intake")
def get_food_intake(db: Session = Depends(get_db)):
    food_intake = db.query(FoodIntake).all()
    return food_intake

@router.post("/food_intake")
def log_food_intake(food_intake: FoodIntake, db: Session = Depends(get_db)):
    db.add(food_intake)
    db.commit()
    return {"message": "Food intake logged successfully"}

@router.get("/physical_activity")
def get_physical_activity(db: Session = Depends(get_db)):
    physical_activity = db.query(PhysicalActivity).all()
    return physical_activity

@router.post("/physical_activity")
def log_physical_activity(physical_activity: PhysicalActivity, db: Session = Depends(get_db)):
    db.add(physical_activity)
    db.commit()
    return {"message": "Physical activity logged successfully"}

@router.get("/food_database")
def get_food_database(db: Session = Depends(get_db)):
    food_database = db.query(FoodDatabase).all()
    return food_database

@router.post("/food_database")
def add_food_database(food_database: FoodDatabase, db: Session = Depends(get_db)):
    db.add(food_database)
    db.commit()
    return {"message": "Food added to database successfully"}

@router.put("/food_database/{id}")
def update_food_database(id: int, food_database: FoodDatabase, db: Session = Depends(get_db)):
    db.query(FoodDatabase).filter(FoodDatabase.id == id).update(food_database.dict())
    db.commit()
    return {"message": "Food updated in database successfully"}

@router.delete("/food_database/{id}")
def delete_food_database(id: int, db: Session = Depends(get_db)):
    db.query(FoodDatabase).filter(FoodDatabase.id == id).delete()
    db.commit()
    return {"message": "Food deleted from database successfully"}
