from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import models
from backend.database import engine
from backend.routes import router as items_router

# Create database tables on startup if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI React Item Manager",
    description="A simple API for managing items with a React frontend.",
    version="1.0.0",
)

# CORS configuration for frontend
# Allows requests from the React development server
origins = [
    "http://localhost:3000",  # React app default port
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(items_router)

@app.get("/", tags=["root"]) # Added tags for better OpenAPI documentation
def read_root():
    return {"message": "Welcome to the FastAPI Item Manager API!"}

# To run the backend:
# 1. Navigate to the `backend` directory.
# 2. Install dependencies: `pip install -r requirements.txt`
# 3. Run the server: `uvicorn main:app --reload`
