from pydantic import BaseModel, constr, Field
from datetime import datetime
from typing import Optional


class RoleModel(BaseModel):
    id: int = Field(default=None)
    company_id: int = Field(default=None)
    created_by_id: int = Field(default=None)
    name: constr(min_length=3, max_length=50)
    description: Optional[constr(max_length=200)] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    users_read: bool
    users_manage: bool
    inventory_read: bool
    inventory_manage: bool
    services_read: bool
    services_manage: bool
    items_read: bool
    items_manage: bool
    payments_read: bool
    payments_manage: bool

    class Config:
        json_schema_extra = {
            "example": {
                "company_id": 1,
                "name": "Manager",
                "description": "Manager role with extensive permissions",
                "users_read": True,
                "users_manage": True,
                "inventory_read": True,
                "inventory_manage": True,
                "services_read": True,
                "services_manage": True,
                "items_read": True,
                "items_manage": True,
                "payments_read": True,
                "payments_manage": True,
                "created_at": "2023-12-08T12:00:00",
                "created_by": 2
            }
        }


class AssignedRole(BaseModel):
    user_id: int
    role_id: int

