from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from enum import Enum


class CompanyPositions(Enum):
    EMPLOYEE = 1
    MANAGER = 2
    OWNER = 3


class UserModel(BaseModel):
    # Main authentication data
    id : int
    email : EmailStr
    password : str

    # Company functionality data
    company_id : int = Field(default = None)
    position : CompanyPositions = Field(default = None)
    roles : List[int] = Field(default = None)

    # Extra user information
    created_at : datetime
    phone_number : str
    first_name : str
    last_name : str
    address : str


class UserRegisterModel(BaseModel):
    email : EmailStr
    password : str

    company_id : int = Field(default = None)
    position : CompanyPositions = Field(default = None)

    phone_number : str
    first_name : str
    last_name : str
    address : str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "abc",
                "company_id": 10,
                "position": 1,
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


class CompleteUserDataModel(BaseModel):
    id : int
    email : EmailStr

    company_id : int = Field(default = None)
    position : CompanyPositions = Field(default = None)
    roles : List[int] = Field(default = None)

    created_at : datetime
    phone_number : str
    first_name : str
    last_name : str
    address : str


class UserUpdateModel(BaseModel):
    phone_number : str = Field(default = None)
    first_name : str = Field(default = None)
    last_name : str = Field(default = None)
    address : str = Field(default = None)

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+4467891",
                "first_name": "Gray",
                "last_name": "Taker",
                "address": "Kaunas, Kauno g. 27g."
            }
        }


class UserAuthenticationDataModel(BaseModel):
    id : int
    email : EmailStr
    password : str


class AdminDataModel(BaseModel):
    user_id: int
    created_at: datetime


class UserCompanyDataModel(BaseModel):
    user_id : Optional[int]
    company_id : Optional[int]
    position : Optional[CompanyPositions]


class UserRegularDataModel(BaseModel):
    id : int
    email : EmailStr

    created_at : datetime
    phone_number : str
    first_name : str
    last_name : str
    address : str
