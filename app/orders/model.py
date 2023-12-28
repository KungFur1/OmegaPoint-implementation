from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from enum import Enum

class OrderStatuses(Enum):
    PENDING = 1
    CONFIRMED = 2
    DELIVERED = 3
    CANCELLED = 4

class OrderModel(BaseModel):
    id : int
    user_id : int
    assignee_id : Optional[int] = Field(default=None)
    company_id : int
    products : List[int]
    quantities : List[int]
    total_price : float
    created_at : datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
    status : OrderStatuses

class OrderPostModel(BaseModel):
    assignee_id : Optional[int] = Field(default=None)
    products: List[int]
    quantities: List[int] 
    created_at : datetime = Field(default_factory=lambda: datetime.now())
    status : OrderStatuses

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "assignee_id": None,
                "products": [1, 5],
                "quantities": [5, 3], 
                "status": OrderStatuses.PENDING
            }
        }


class OrderUpdateModel(BaseModel):
    company_id : int
    assignee_id : Optional[int] = Field(default=None)
    products: List[int]
    quantities: List[int] 
    status : OrderStatuses
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "company_id": 1,
                "assignee_id": None,
                "products": [1, 5],
                "quantities": [5, 3], 
                "status": OrderStatuses.PENDING
            }
        }


class DiscountModel(BaseModel):
    name : str
    order_id : int
    percentage_discount : Optional[float] = Field(default=None)
    amount_discount : Optional[float] = Field(default=None)
    created_at : datetime = Field(default_factory=lambda: datetime.now())

    class Config:
        json_schema_extra = {
            "example": {
                "name": "10 euros discount",
                "order_id": 1,
                "percentage_discount": None,
                "amount_discount": 10
            }
        }


class AddOrderItemModel(BaseModel):
    item_id : int
    quantity : int

    class Config:
        json_schema_extra = {
            "example": {
                "item_id": 1,
                "quantity": 5
            }
        }
    

class OrderItemModel(BaseModel):
    id : int
    order_id : int
    item_id : int
    asignee_id : Optional[int] = Field(default=None)
    quantity : int
    status : Optional[OrderStatuses] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "order_id": 1,
                "item_id": 1,
                "asignee_id": None,
                "quantity": 5,
                "status": None
            }
        }