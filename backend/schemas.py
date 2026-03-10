from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Optional

class CalculationBase(BaseModel):
    expression: str = Field(..., example="2 + 2 * (3 - 1)", description="The mathematical expression to evaluate.")
    unit_mode: Optional[str] = Field("degrees", example="degrees", pattern="^(degrees|radians)$", description="The unit mode for trigonometric functions (degrees or radians).")

class CalculationCreate(CalculationBase):
    """Schema for incoming calculation requests."""
    pass

class CalculationResponse(BaseModel):
    """Schema for a successful calculation response."""
    result: str = Field(..., example="6", description="The calculated result.")
    historyId: uuid.UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef", description="The ID of the recorded calculation in history.")

class CalculationHistoryItem(CalculationBase):
    """Schema for an item in the calculation history."""
    id: uuid.UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")
    result: str = Field(..., example="6")
    timestamp: datetime = Field(..., example="2023-10-27T10:00:00Z")

    class Config:
        # Enable ORM mode for SQLAlchemy compatibility, allowing Pydantic to read data from ORM objects.
        orm_mode = True 
        from_attributes = True # Pydantic v2 equivalent of orm_mode

