from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class StoreModel(BaseModel):
    id: int = Field(default=None)
    company_id: int
    name: str
    location: str
    created_at: datetime = Field(default=None)

class StoreCreateModel(BaseModel):
    name: str
    location: str

class StoreUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)

