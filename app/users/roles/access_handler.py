from pydantic import BaseModel, Field
import app.users.roles.db as roles_db
import app.users.db as users_db
from app.users.model import CompanyPositions, UserCompanyDataModel
from typing import List
from app.users.roles.model import RoleModel


class AccessModel(BaseModel):
    users_read: bool = Field(default=False)
    users_manage: bool = Field(default=False)
    inventory_read: bool = Field(default=False)
    inventory_manage: bool = Field(default=False)
    services_read: bool = Field(default=False)
    services_manage: bool = Field(default=False)
    items_read: bool = Field(default=False)
    items_manage: bool = Field(default=False)
    payments_read: bool = Field(default=False)
    payments_manage: bool = Field(default=False)


def get_user_access(user_id: int) -> AccessModel:
    # Check if user is owner or manager, they have access to everything
    user_company_data = users_db.get_user_company_data(user_id=user_id)
    if user_company_data is not None and (user_company_data.position == CompanyPositions.MANAGER or user_company_data.position == CompanyPositions.OWNER):
        return AccessModel(users_read=True, users_manage=True, inventory_read=True, inventory_manage=True, services_read=True, 
                           services_manage=True, items_read=True, items_manage=True, payments_read=True, payments_manage=True)

    # If user is employee
    assigned_roles = roles_db.get_assgined_roles_by_user_id(user_id=user_id)
    roles: List[RoleModel] = []
    for assigned_role in assigned_roles:
        roles.append(roles_db.get_role_by_id(assigned_role.role_id))
    
    access = AccessModel()
    for role in roles:
        if role.inventory_manage:
            access.inventory_manage = True
        if role.inventory_read:
            access.inventory_read = True

        if role.items_manage:
            access.items_manage = True
        if role.items_read:
            access.items_read = True

        if role.payments_manage:
            access.payments_manage = True
        if role.payments_read:
            access.payments_read = True

        if role.services_manage:
            access.services_manage = True
        if role.services_read:
            access.services_read = True

        if role.users_manage:
            access.users_manage = True
        if role.users_read:
            access.users_read = True

    return access
