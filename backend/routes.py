from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from . import models, schemas
from .database import SessionLocal
from .utils import evaluate_expression

# Create an API router
router = APIRouter()

# Dependency to get the DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health", response_model=schemas.BaseModel, summary="Health Check")
async def health_check():
    """Returns the API status and current timestamp."""
    return {"status": "UP", "timestamp": datetime.now().isoformat()}

@router.post("/calculate", response_model=schemas.CalculationResponse, status_code=status.HTTP_201_CREATED, summary="Perform and Log Calculation")
async def calculate_and_log(
    calculation_data: schemas.CalculationCreate,
    db: Session = Depends(get_db)
):
    """Processes a mathematical expression, performs the calculation, and logs it to the database."""
    try:
        # Evaluate the expression using the utility function
        result_str = evaluate_expression(calculation_data.expression, calculation_data.unit_mode)

        # Create a new Calculation entry in the database
        db_calculation = models.Calculation(
            expression=calculation_data.expression,
            result=result_str,
            unit_mode=calculation_data.unit_mode
        )
        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation) # Refresh to get the generated ID and timestamp

        return {"result": result_str, "historyId": db_calculation.id}
    except ValueError as e:
        # Handle specific calculation/validation errors
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Catch any other unexpected errors and roll back the transaction
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error during calculation or logging: {e}")

@router.get("/history", response_model=List[schemas.CalculationHistoryItem], summary="Get Calculation History")
async def get_calculation_history(db: Session = Depends(get_db)):
    """Retrieves the list of past calculations, ordered by timestamp (most recent first)."""
    # Query the database for all calculations, ordered by timestamp descending, limited to 100 items.
    history = db.query(models.Calculation).order_by(models.Calculation.timestamp.desc()).limit(100).all()
    return history

