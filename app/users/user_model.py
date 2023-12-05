from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    fullname : str = Field(default = None)
    email : EmailStr  = Field(default = None)
    password : str = Field(default = None)
    class Config:
        json_schema_extra = {
            "user_demo" : {
                "name" : "Bek",
                "email" : "help@bekbrace.com",
                "password" : "pass"
            }
        }


class UserLoginSchema(BaseModel):
    email : EmailStr  = Field(default = None)
    password : str = Field(default = None)
    class Config:
        json_schema_extra = {
            "user_demo" : {
                "email" : "help@bekbrace.com",
                "password" : "pass"
            }
        }
