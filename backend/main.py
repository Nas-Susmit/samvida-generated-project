# FastAPI App
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi import status
from routes import router
from database import engine
import models

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the backend"}

app.include_router(router)
