from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from . import database, routes

# Load environment variables from .env file (if present)
load_dotenv()

# Create database tables on application startup
# This ensures the database schema is ready when the app starts
database.create_db_tables()

app = FastAPI(
    title="Scientific Calculator API",
    description="A RESTful API for performing scientific calculations and logging their history. "
                "Uses FastAPI, SQLite, and SQLAlchemy.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This is essential for the React frontend to communicate with the FastAPI backend
# when they are served from different origins (e.g., localhost:3000 and localhost:8000).
origins = [
    "http://localhost",
    "http://localhost:3000",  # React's default development server port
    # Add other frontend deployment URLs here, e.g., "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Specifies which origins are allowed to make requests
    allow_credentials=True,      # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],         # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],         # Allow all headers in cross-origin requests
)

# Include the API routes defined in routes.py
app.include_router(routes.router)

@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint, redirects to API documentation."""
    return {"message": "Scientific Calculator API is running. Go to /docs for API documentation."}

