# Import required libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import uvicorn
import sqlite3
from backend.database import create_connection, create_table
from backend.models import User, FoodItem, FoodLog, WeightLog
from backend.routes import user_router, food_item_router, food_log_router, weight_log_router

# Create the FastAPI application
app = FastAPI()

# Create the database connection and tables
create_connection()
create_table('users', User)
create_table('food_items', FoodItem)
create_table('food_logs', FoodLog)
create_table('weight_logs', WeightLog)

# Include the routers
app.include_router(user_router)
app.include_router(food_item_router)
app.include_router(food_log_router)
app.include_router(weight_log_router)

# Run the application
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
