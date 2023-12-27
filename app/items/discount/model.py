from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemDiscountModel(BaseModel):
    discount_id: int = Field(default=None)
    item_id: int
    discount_amount: float


class ItemDiscountCreateModel(BaseModel):
    item_id: int
    discount_amount: float

    class Config:
        json_schema_extra = {
            "example": {
                "item_id": 1,
                "discount_amount": 5.0
            }
        }