from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AppointmentModel(BaseModel):
    id: int = Field(default = None)
    service_id: int
    company_id: int
    user_id: int 
    appointment_date: datetime
    price: float
    created_at : datetime = Field(default = None)

class AppointmentPostModel(BaseModel):
    service_id: int
    user_id: int
    appointment_date: datetime
    price: float
    
class AppointmentUpdateModel(BaseModel):
    service_id: Optional[int] = Field(default = None)
    user_id: Optional[int] = Field(default = None)
    appointment_date: Optional[datetime] = Field(default = None)
    price: Optional[float] = Field(default = None)
