from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemModel(BaseModel):
    item_id: int = Field(default=None)
    name: str
    description: str
    price: float
    tax_percentage: float


class ItemCreateModel(BaseModel):
    name: str
    description: str
    price: float
    tax_percentage: float

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Classic Facial",
                "description": "A basic facial treatment",
                "price": 50.0,
                "tax_percentage": 5.0
            }
        }


class ItemUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    tax_percentage: Optional[float] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Facial",
                "description": "An updated facial treatment",
                "price": 60.0,
                "tax_percentage": 6.0
            }
        }
