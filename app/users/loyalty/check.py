from fastapi import HTTPException
from app.users.loyalty.model import LoyaltyModel
from app.users.model import UserCompanyDataModel
import app.users.loyalty.db as db


def loyalty_matches_company(loyalty: LoyaltyModel, company_user_data: UserCompanyDataModel):
    if loyalty is None or company_user_data is None or (loyalty.company_id != company_user_data.company_id):
        raise HTTPException(status_code=400, detail="loyalty_matches_company CHECK: failed")
