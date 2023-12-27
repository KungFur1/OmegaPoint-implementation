from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InventoryModel(BaseModel):
    inventory_id: int = Field(default=None)
    item_id: int
    store_id: int
    quantity: int


class InventoryCreateModel(BaseModel):
    item_id: int
    store_id: int
    quantity: int

    class Config:
        json_schema_extra = {
            "example": {
                "item_id": 1,
                "store_id": 2,
                "quantity": 100
            }
        }
        
class InventoryUpdateModel(BaseModel):
    quantity: Optional[int] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "quantity": 150
            }
        }