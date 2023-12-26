from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from enum import Enum

class OrderModel(BaseModel):
    id : int
    user_id : int
    company_id : int
    products : List[int]
    quantities : List[int]
    total_price : float
    created_at : datetime
    status : int

class OrderPostModel(BaseModel):
    user_id : int
    company_id : int
    total_price : float
    created_at : datetime = Field(default_factory=lambda: datetime.now())
    status : int

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "company_id": 1,
                "total_price": 10.0,
                "Created_at": "2021-09-11 12:00:00",
                "status": 1,
            }
        }
