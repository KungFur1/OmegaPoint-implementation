import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.company.model import CompanyCreateModel
import app.company.db as db
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
    # Not implemented yet
    return {}


@router.post("/cinematic/company", tags=["company"], status_code=201)
@handle_db_error
async def create_company(company_data : CompanyCreateModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    users_check.is_admin(user_id=user_identification.id)

    db.post_company(company_data)
    return {"info" : "company succesfully inserted"}


@router.put("/cinematic/company", tags=["company"], status_code=201)
@handle_db_error
async def edit_company(company_data : CompanyCreateModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Not implemented yet
    return {}


@router.delete("/cinematic/company", tags=["company"], status_code=204)
@handle_db_error
async def delete_company(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Not implemented yet
    return {}