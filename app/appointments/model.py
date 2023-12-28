from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AppointmentModel(BaseModel):
    id: int = Field(default = None)
    name: str
    company_id: int
    user_id: int 
    appointment_date: datetime
    price: float
    created_at : datetime = Field(default = None)

class AppointmentPostModel(BaseModel):
    name: str
    user_id: int
    appointment_date: datetime
    price: float
    
class AppointmentUpdateModel(BaseModel):
    name: Optional[str] = Field(default = None)
    user_id: Optional[int] = Field(default = None)
    appointment_date: Optional[datetime] = Field(default = None)
    price: Optional[float] = Field(default = None)
