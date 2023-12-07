# {"data" : data} - when returning some data
# {"info" : success_message} - when some operation was successful
# raise fastapi.HTTPException - when something is wrong, provide detail
# all messages should start with non-capital letter and end without a dot
# {"token" : token} - after succesful login
import fastapi
from app.JWT_auth.user_identification import UserIdentification # Authorization!
from app.JWT_auth.authorization import authorization_wrapper # Authorization!
from app.company.model import CompanyModel
import app.company.db as db
import app.users.db as users_db
from mysql.connector import Error as DBError

router = fastapi.APIRouter()


@router.get("/cinematic/company", tags=["company"])
async def get_all_companies():
    try:
        return {"data" : db.get_all_companies()}
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")


@router.get("/cinematic/company/{company_id}", tags=["company"])
async def get_company_by_id(company_id : int):
    # Not implemented yet
    return {}


@router.post("/cinematic/company", tags=["company"], status_code=201)
async def create_company(company_data : CompanyModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    try:
        if users_db.get_admin_information(user_id=user_identification.id):
            db.post_company(company_data)
            return {"info" : "company succesfully inserted"}
        else:
            raise fastapi.HTTPException(status_code=400, detail="you must be admin user to create a company")
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")


@router.delete("/cinematic/company", tags=["company"])
async def delete_company(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Not implemented yet
    return {}