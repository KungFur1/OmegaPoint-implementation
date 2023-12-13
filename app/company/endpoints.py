import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.company.model import CompanyModel
import app.company.db as db
import app.users.db as users_db
from mysql.connector import Error as DBError
from app.db_error_handler import handle_db_error

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
async def create_company(company_data : CompanyModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    if users_db.get_admin_information_by_id(user_id=user_identification.id) is None:
        raise fastapi.HTTPException(status_code=400, detail="you must be admin user to create a company")
    db.post_company(company_data)
    return {"info" : "company succesfully inserted"}


@router.put("/cinematic/company", tags=["company"], status_code=201)
@handle_db_error
async def edit_company(company_data : CompanyModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Not implemented yet
    return {}


@router.delete("/cinematic/company", tags=["company"], status_code=204)
@handle_db_error
async def delete_company(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Not implemented yet
    return {}