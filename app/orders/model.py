from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class OrderStatuses(Enum):
    PENDING = 1
    CONFIRMED = 2
    DELIVERED = 3
    CANCELLED = 4
    PAID = 5
    REFUNDED = 6
    VOIDED = 7    

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
    status : OrderStatuses = Field(default=OrderStatuses.PENDING.value)

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "products": [1, 5],
                "quantities": [5, 3], 
            }
        }


class OrderUpdateModel(BaseModel):
    assignee_id : Optional[int] = Field(default=None)
    products: List[int]
    quantities: List[int] 
    status : OrderStatuses
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())

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