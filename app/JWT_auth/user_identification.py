from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from app.users.model import CompanyPositions
from app.users.roles.access_handler import AccessModel
from typing import Optional


# Users authorized information, returned by authorization_wrapper
class UserIdentification:
    def __init__(self, id : int, email : str) -> None:
        self.id = id
        self.email = email
        

# Complete user information, returned by get_complete_user_information
class CompleteUserInformation(BaseModel):
    id : int
    email : EmailStr

    company_id : Optional[int] = Field(default = None)
    position : Optional[CompanyPositions] = Field(default=None)
    access : Optional[AccessModel] = Field(default = None)

    created_at : datetime
    phone_number : str
    first_name : str
    last_name : str
    address : str
