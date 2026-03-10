# Import necessary libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from database import engine

app = FastAPI()

# Add CORS middleware
cors_origins = [
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routes
app.include_router(router)

# Run the database migrations
with engine.connect() as con:
    con.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL, daily_calorie_goals INTEGER NOT NULL)")
    con.execute("CREATE TABLE IF NOT EXISTS food_intake (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, food_name TEXT NOT NULL, calories INTEGER NOT NULL, date DATE NOT NULL)")
    con.execute("CREATE TABLE IF NOT EXISTS food_database (id INTEGER PRIMARY KEY, food_name TEXT NOT NULL, calories INTEGER NOT NULL)")
