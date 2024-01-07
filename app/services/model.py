from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ServiceModel(BaseModel):
    id: int = Field(default = None)
    name: str
    company_id: int
    description: str
    price: float
    created_at : datetime = Field(default = None)

class ServicePostModel(BaseModel):
    name: str
    company_id: int
    description: str
    price: float

    class Config:
        json_schema_extra = {
            "example": {
                "name" : "serviceName",
                "company_id" : "1",
                "description" : "Service description",
                "price" : 10.88,
            }
        }
    
class ServiceUpdateModel(BaseModel):
    name: Optional[str] = Field(default = None)
    description: Optional[str] = Field(default = None)
    price: Optional[float] = Field(default = None)
    

class ServiceAvailabilityModel(BaseModel):
    service_id: int 
    start_date: datetime
    end_date: datetime
    

