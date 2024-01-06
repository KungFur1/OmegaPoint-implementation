from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemDiscountModel(BaseModel):
    discount_id: int = Field(default=None)
    item_id: int
    discount_amount_percentage: float


class ItemDiscountCreateModel(BaseModel):
    discount_amount_percentage: float

    class Config:
        json_schema_extra = {
            "example": {
                "discount_amount_percentage": 5.0
            }
        }