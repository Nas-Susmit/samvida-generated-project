# Import required libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from backend.database import engine
from backend.models import User, Food
from backend.routes import user_routes, food_routes

# Create FastAPI app
app = FastAPI()

# Include routes
app.include_router(user_routes)
app.include_router(food_routes)

# Define a route for the root of the API
@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
