from pydantic import BaseModel, Field
from datetime import datetime, time, date, timedelta
from typing import Optional


class AppointmentModel(BaseModel):
    id: int = Field(default = None)
    service_id: int
    company_id: int
    user_id: int 
    appointment_date: date
    start_time: time
    end_time: time
    price: float
    created_at : datetime = Field(default = None)

class AppointmentPostModel(BaseModel):
    service_id: int
    company_id: int
    user_id: int
    appointment_date: date
    start_time: time
    end_time: time
    price: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "service_id" : "1",
                "company_id" : "1",
                "user_id" : "1",
                "appointment_date" : "2024-01-01",
                "start_time" : "00:00:00",
                "end_time" : "00:00:00",
                "price" : 0,
            }
        }
    
class AppointmentUpdateModel(BaseModel):
    service_id: Optional[int] = Field(default = None)
    user_id: Optional[int] = Field(default = None)
    appointment_date: Optional[date] = Field(default = None)
    start_time: Optional[time] = Field(default = None)
    end_time: Optional[time] = Field(default = None)
    price: Optional[float] = Field(default = None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "service_id" : "1",
                "user_id" : "1",
                "appointment_date" : "2024-01-01",
                "start_time" : "00:00:00",
                "end_time" : "00:00:00",
                "price" : 0,
            }
        }

class AppointmentsList(BaseModel):
    id: int = Field(default=None)
    appointment_date: date
    start_time: time
    end_time: time