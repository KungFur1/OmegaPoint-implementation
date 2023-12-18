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


class CompanyUpdateModel(BaseModel):
    email: EmailStr = Field(default=None)
    name: str = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "UpdateUser@example.com",
                "name": "UAB Up to date"
            }
        }