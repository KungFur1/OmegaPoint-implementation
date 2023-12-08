# Roles CRUD is only accessible to managers and owners of the company.
import fastapi
from app.JWT_auth.user_identification import UserIdentification # Authorization!
from app.JWT_auth.authorization import authorization_wrapper # Authorization!
import app.users.roles.model as db
from mysql.connector import Error as DBError
from app.users.roles.model import RoleModel

router = fastapi.APIRouter()


@router.get("/cinematic/company/roles", tags=["users", "roles"], status_code=200)
async def get_all_company_roles(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Check if user is owner or manager, check if user belongs to that company.
    # If user is, then retrieve all company roles from db and return
    return {}


@router.get("/cinematic/company/roles/{role_id}", tags=["users", "roles"], status_code=200)
async def get_role_by_id(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Retrieve the role`s company_id
    # Check if user is owner or manager, check if user belongs to that company.
    # If user is, return the role
    return {}


@router.post("/cinematic/company/roles", tags=["users", "roles"], status_code=201)
async def upload_role(role_data : RoleModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Check if user is owner or manager
    # Post role to database
    return {}


@router.put("/cinematic/company/roles/{role_id}", tags=["users", "roles"], status_code=200)
async def update_role(role_data : RoleModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Retrieve the role`s company_id
    # Check if user is owner or manager, check if user belongs to that company.
    # If user is, update the role in database
    return {}


@router.delete("/cinematic/company/roles/{role_id}", tags=["users", "roles"], status_code=204)
async def delete_role(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Retrieve the role`s company_id
    # Check if user is owner or manager, check if user belongs to that company.
    # If user is, delete the role
    return {}