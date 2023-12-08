from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List
from enum import Enum


class CompanyPositions(Enum):
    EMPLOYEE = 1
    MANAGER = 2
    OWNER = 3


class UserModel(BaseModel):
    # Main authentication data (Required in registration)
    id : int  = Field(default=None)
    email : EmailStr  = Field(default = None)
    password : str = Field(default = None)

    # Company functionality data
    company_id : int = Field(default = None)
    position : CompanyPositions = Field(default=CompanyPositions.EMPLOYEE)
    roles : List[int] = Field(default = None)

    # Extra user information
    created_at : datetime = Field(default=None)
    # (Optional, but needed in registration)
    phone_number : str = Field(default = None)
    first_name : str = Field(default = None)
    last_name : str = Field(default = None)
    address : str = Field(default = None)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 12345,
                "email": "user@example.com",
                "password": "abc",
                "position": 1,
                "roles": [1, 2, 3],
                "company_id": 10,
                "created_at": "2023-12-05T00:00:00",
                "phone_number": "+1234567890",
                "first_name": "Ben",
                "last_name": "Taker",
                "address": "Vilnius, Pylimo g. 24a"
            }
        }


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "abc"
            }
        }


class UserAuthenticationDataModel(BaseModel):
    id : int
    email : EmailStr
    password : str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 12345,
                "email": "user@example.com",
                "password": "abc",
            }
        }


class AdminInformationModel(BaseModel):
    user_id: int
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 2,
                "created_at": "2023-12-05T00:00:00"
            }
        }


class UserCompanyDataModel(BaseModel):
    user_id : int
    company_id : int
    position : CompanyPositions

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 931,
                "company_id": 16,
                "position": 2,
            }
        }