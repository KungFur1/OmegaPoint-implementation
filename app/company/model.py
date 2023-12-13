from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class CompanyModel(BaseModel):
    id: int = Field(default=None)
    email: EmailStr
    name: str
    created_at: datetime = Field(default=None)


class CompanyCreateModel(BaseModel):
    email: EmailStr
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "UAB gpt technologies"
            }
        }