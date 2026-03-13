# FastAPI routes definition
from fastapi import APIRouter
from models import User
router = APIRouter()
@router.get('/users')
def get_users():
    return [{'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}]
