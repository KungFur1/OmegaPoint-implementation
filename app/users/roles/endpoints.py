# Roles CRUD is only accessible to managers and owners of the company.
import fastapi
from app.JWT_auth.user_identification import UserIdentification # Authorization!
from app.JWT_auth.authorization import authorization_wrapper # Authorization!
import app.users.roles.db as db
import app.users.db as users_db
from mysql.connector import Error as DBError
from app.users.model import CompanyPositions
from app.users.roles.model import RoleModel

router = fastapi.APIRouter()


@router.get("/cinematic/roles/company", tags=["users", "roles"], status_code=200)
async def get_roles_comp(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    try:
        user_company_data = users_db.get_user_company_data(user_id=user_identification.id)
        if user_company_data and (user_company_data.position == CompanyPositions.MANAGER or user_company_data.position == CompanyPositions.OWNER):
            return {"data" : db.get_company_roles(company_id=user_company_data.company_id)}
        else:
            raise fastapi.HTTPException(status_code=400, detail="you must be manager or owner to acccess company roles")
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")


@router.get("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=200)
async def get_role_by_id(role_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Retrieve the role`s company_id
    # Check if user is owner or manager, check if user belongs to that company.
    # If user is, return the role
    return {}


@router.post("/cinematic/roles/company", tags=["users", "roles"], status_code=201)
async def upload_role(role_data : RoleModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Check if user is owner or manager
    # Post role to database
    return {}


@router.put("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=200)
async def update_role(role_id: int, role_data : RoleModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Retrieve the role`s company_id
    # Check if user is owner or manager, check if user belongs to that company.
    # If user is, update the role in database
    return {}


@router.delete("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=204)
async def delete_role(role_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Retrieve the role`s company_id
    # Check if user is owner or manager, check if user belongs to that company.
    # If user is, delete the role
    return {}
