from fastapi import HTTPException
from app.users.roles.model import RoleModel
from app.users.model import UserCompanyDataModel
import app.users.roles.db as db


def role_is_same_company(role: RoleModel, user_company_data: UserCompanyDataModel):
    if role is None or user_company_data is None or user_company_data.company_id != role.company_id:
        raise HTTPException(status_code=400, detail="role_is_same_company CHECK: failed")


def role_is_not_assigned(role_id: int, user_id: int):
    if db.get_assigned_role(user_id=user_id, role_id=role_id) is not None:
        raise HTTPException(status_code=400, detail="role_is_not_assigned CHECK: failed")
