from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class CompanyModel(BaseModel):
    id: int = Field(default=None)
    email: EmailStr
    name: str
    created_at: datetime = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 57,
                "email": "user@example.com",
                "name": "UAB gpt technologies",
                "created_at": "2023-12-05T00:00:00"
            }
        }