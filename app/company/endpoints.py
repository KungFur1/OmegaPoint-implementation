import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.company.model import CompanyCreateModel, CompanyUpdateModel
import app.company.db as db
import app.users.db as users_db
from app.db_error_handler import handle_db_error
import app.company.check as check
import app.users.check as users_check

router = fastapi.APIRouter()


@router.get("/cinematic/company", tags=["company"], status_code=200)
@handle_db_error
async def get_all_companies():
    return {"data" : db.get_all_companies()}


@router.get("/cinematic/company/{company_id}", tags=["company"], status_code=200)
@handle_db_error
async def get_company_by_id(company_id : int):
    return {"data" : db.get_company_by_id(company_id=company_id)}


@router.post("/cinematic/company", tags=["company"], status_code=201)
@handle_db_error
async def create_company(company_create_data : CompanyCreateModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    users_check.is_admin(user_id=user_identification.id)

    db.post_company(company_create_data)
    return {"info" : "company successfully inserted"}


@router.put("/cinematic/company", tags=["company"], status_code=201)
@handle_db_error
async def edit_company(company_update_data : CompanyUpdateModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)

    users_check.is_owner(user_company_data=auth_user_cd)

    db.put_company(auth_user_cd.company_id, company_update_data)
    return {"info" : "company successfully updated"}


@router.delete("/cinematic/company", tags=["company"], status_code=204)
@handle_db_error
async def delete_company(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)

    users_check.is_owner(user_company_data=auth_user_cd)

    db.delete_company(company_id=auth_user_cd.company_id)
    return {"info" : "company successfully deleted"}
