from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemModel(BaseModel):
    item_id: int = Field(default=None)
    company_id: int
    name: str
    description: str
    price: float
    tax_percentage: float


class ItemCreateModel(BaseModel):
    # company_id: int
    name: str
    description: str
    price: float
    tax_percentage: float

    class Config:
        json_schema_extra = {
            "example": {
                # "company_id": 1,
                "name": "Item x",
                "description": "Description x",
                "price": 10,
                "tax_percentage": 2
            }
        }


class ItemUpdateModel(BaseModel):
    company_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    tax_percentage: Optional[float] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "company_id": 1,
                "name": "Item x",
                "description": "Description x",
                "price": 10,
                "tax_percentage": 2
            }
        }
