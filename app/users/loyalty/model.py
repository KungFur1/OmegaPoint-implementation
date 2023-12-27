from pydantic import BaseModel, constr, Field
from typing import Optional
from datetime import datetime


class LoyaltyModel(BaseModel):
    id : int
    company_id: int
    created_by_id: int
    name: constr(min_length=3, max_length=50)
    description: Optional[constr(max_length=200)]
    created_at : datetime

    discount_percent : float


class LoyaltyCreateModel(BaseModel):
    company_id: int = Field(default=None)
    created_by_id: int = Field(default=None)

    name: constr(min_length=3, max_length=50)
    description: Optional[constr(max_length=200)]

    discount_percent : float

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Old customer",
                "description": "This loyalty should only be applied only to the most loyal customers out there!",
                "discount_percent": 23.5
            }
        }