# Import necessary libraries
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from models import User, FoodIntake, FoodDatabase
from sqlalchemy.orm import sessionmaker
from database import engine

router = APIRouter()

# Create a new user
@router.post("/users")
def create_user(request: Request):
    user_data = request.json
    new_user = User(username=user_data['username'], password=user_data['password'], daily_calorie_goals=user_data['daily_calorie_goals'])
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(new_user)
    session.commit()
    session.close()
    return JSONResponse(content={"message": "User created successfully"}, status_code=201)

# Get user details
@router.get("/users/{user_id}")
def get_user_details(user_id: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content=user.__dict__, status_code=200)

# Update user details
@router.put("/users/{user_id}")
def update_user_details(user_id: int, request: Request):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = request.json
    user.username = user_data['username']
    user.password = user_data['password']
    user.daily_calorie_goals = user_data['daily_calorie_goals']
    session.commit()
    session.close()
    return JSONResponse(content={"message": "User details updated successfully"}, status_code=200)

# Log daily food intake
@router.post("/food-intake")
def log_food_intake(request: Request):
    food_intake_data = request.json
    new_food_intake = FoodIntake(user_id=food_intake_data['user_id'], food_name=food_intake_data['food_name'], calories=food_intake_data['calories'], date=food_intake_data['date'])
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(new_food_intake)
    session.commit()
    session.close()
    return JSONResponse(content={"message": "Food intake logged successfully"}, status_code=201)

# Get user's food intake history
@router.get("/food-intake/{user_id}")
def get_food_intake_history(user_id: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    food_intake = session.query(FoodIntake).filter(FoodIntake.user_id == user_id).all()
    session.close()
    return JSONResponse(content=[food.__dict__ for food in food_intake], status_code=200)

# Get all food items in database
@router.get("/food-database")
def get_all_food_items():
    Session = sessionmaker(bind=engine)
    session = Session()
    food_database = session.query(FoodDatabase).all()
    session.close()
    return JSONResponse(content=[food.__dict__ for food in food_database], status_code=200)

# Add new food item to database (admin only)
@router.post("/food-database")
def add_new_food_item(request: Request):
    food_item_data = request.json
    new_food_item = FoodDatabase(food_name=food_item_data['food_name'], calories=food_item_data['calories'])
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(new_food_item)
    session.commit()
    session.close()
    return JSONResponse(content={"message": "Food item added successfully"}, status_code=201)

# Get user's progress reports
@router.get("/progress-reports/{user_id}")
def get_progress_reports(user_id: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    food_intake = session.query(FoodIntake).filter(FoodIntake.user_id == user_id).all()
    progress_reports = []
    for food in food_intake:
        progress_reports.append({"date": food.date, "calories": food.calories})
    session.close()
    return JSONResponse(content=progress_reports, status_code=200)

# Get personalized nutrition advice for user
@router.get("/nutrition-advice/{user_id}")
def get_nutrition_advice(user_id: int):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    food_intake = session.query(FoodIntake).filter(FoodIntake.user_id == user_id).all()
    total_calories = 0
    for food in food_intake:
        total_calories += food.calories
    session.close()
    if total_calories > user.daily_calorie_goals:
        return JSONResponse(content={"advice": "You have exceeded your daily calorie goals"}, status_code=200)
    elif total_calories < user.daily_calorie_goals:
        return JSONResponse(content={"advice": "You are below your daily calorie goals"}, status_code=200)
    else:
        return JSONResponse(content={"advice": "You are at your daily calorie goals"}, status_code=200)
