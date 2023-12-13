from fastapi import HTTPException
from app.users.model import CompanyPositions, UserCompanyDataModel
import app.users.db as db


def is_admin(user_id: int):
    if db.get_admin_information_by_id(user_id=user_id) is None:
        raise HTTPException(status_code=400, detail="is_admin CHECK: failed")


def is_owner(user_company_data: UserCompanyDataModel):
    if user_company_data is None or user_company_data.position != CompanyPositions.OWNER:
        raise HTTPException(status_code=400, detail="is_owner CHECK: failed")
    

def is_owner_or_manager(user_company_data: UserCompanyDataModel):
    if user_company_data is None or (user_company_data.position != CompanyPositions.OWNER and user_company_data.position != CompanyPositions.MANAGER):
        raise HTTPException(status_code=400, detail="is_owner_or_manager CHECK: failed")


def users_are_same_company(user1_company_data: UserCompanyDataModel, user2_company_data: UserCompanyDataModel):
    if user1_company_data is None or user2_company_data is None or user2_company_data.company_id != user2_company_data.company_id:
        raise HTTPException(status_code=400, detail="users_are_same_company CHECK: failed")