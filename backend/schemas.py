from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    name: str # Name is required for a full update
    is_completed: bool

class Item(ItemBase):
    id: int
    is_completed: bool

    model_config = ConfigDict(from_attributes=True) # Pydantic V2 way
