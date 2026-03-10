# Import required libraries
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from backend.models import User, Food
from backend.database import Session

# Create API routers
user_routes = APIRouter()
food_routes = APIRouter()

# Define routes for users
@user_routes.get("/users")
async def get_users():
    session = Session()
    users = session.query(User).all()
    return JSONResponse(content=[user.__dict__ for user in users])

@user_routes.get("/users/{user_id}")
async def get_user(user_id: int):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    return JSONResponse(content=user.__dict__)

# Define routes for foods
@food_routes.get("/foods")
async def get_foods():
    session = Session()
    foods = session.query(Food).all()
    return JSONResponse(content=[food.__dict__ for food in foods])

@food_routes.get("/foods/{food_id}")
async def get_food(food_id: int):
    session = Session()
    food = session.query(Food).filter_by(id=food_id).first()
    return JSONResponse(content=food.__dict__)
