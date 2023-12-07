import fastapi
from app.company.model import CompanyModel
# Authorization!
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
# Authorization!
import app.company.db as db

router = fastapi.APIRouter()


@router.get("/cinematic/company", tags=["company"])
async def get_all_companies():
    all_companies = db.retrieve_all_companies()
    if all_companies:
        return {"data" : all_companies}
    else:
        raise fastapi.HTTPException(status_code=500, detail="Failed to retrieve companies from database")


@router.get("/cinematic/company/{company_id}", tags=["company"])
async def get_company_by_id(company_id : int):
    # Not implemented yet
    return {}


@router.post("/cinematic/company", tags=["company"], status_code=201)
async def create_company(company_data : CompanyModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    if db.user_is_admin(user_id=user_identification.id):
        if db.insert_company(company_data):
            return {"info" : "company succesfully inserted"}
        else:
            raise fastapi.HTTPException(status_code=500, detail="Failed to insert company into database")
    else:
        raise fastapi.HTTPException(status_code=400, detail="Only an admin user can create a company")


@router.delete("/cinematic/company", tags=["company"])
async def delete_company(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Not implemented yet
    return {}