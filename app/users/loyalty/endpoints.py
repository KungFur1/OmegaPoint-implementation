import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
import app.users.loyalty.db as db
import app.users.db as users_db
from app.db_error_handler import handle_db_error
import app.users.check as users_check
import app.users.loyalty.check as check
from app.users.loyalty.model import LoyaltyCreateModel

router = fastapi.APIRouter()


@router.get("/cinematic/loyalty", tags=["loyalty"], status_code=200)
@handle_db_error
async def get_loyalty(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)

    users_check.belongs_to_company(user_company_data=auth_user_cd)

    return {"data" : db.get_loyalty_by_company_id(company_id=auth_user_cd.company_id)}


@router.get("/cinematic/loyalty/{id}", tags=["loyalty"], status_code=200)
@handle_db_error
async def get_loyalty_by_id(id : int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    loyalty = db.get_loyalty_by_id(loyalty_id=id)

    check.loyalty_matches_company(loyalty=loyalty, company_user_data=auth_user_cd)

    return {"data" : loyalty}


@router.post("/cinematic/loyalty", tags=["loyalty"], status_code=201)
@handle_db_error
async def create_loyalty(loyalty_create_data : LoyaltyCreateModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    
    users_check.is_owner_or_manager(user_company_data=auth_user_cd)

    loyalty_create_data.company_id = auth_user_cd.company_id
    loyalty_create_data.created_by_id = user_identification.id
    db.post_loyalty(loyalty_data=loyalty_create_data)
    return {"info" : "loyalty created successfully"}


@router.delete("/cinematic/loyalty/{id}", tags=["loyalty"], status_code=204)
@handle_db_error
async def delete_loyalty_by_id(id : int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    loyalty = db.get_loyalty_by_id(loyalty_id=id)

    check.loyalty_matches_company(loyalty=loyalty, company_user_data=auth_user_cd)
    users_check.is_owner_or_manager(user_company_data=auth_user_cd)

    db.delete_loyalty_by_id(loyalty_id=id)
    return {"info" : "loyalty deleted successfully"}