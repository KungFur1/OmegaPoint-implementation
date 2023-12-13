# Roles CRUD is only accessible to managers and owners of the company.
import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
import app.users.roles.db as db
import app.users.db as users_db
from mysql.connector import Error as DBError
from app.users.model import CompanyPositions
from app.users.roles.model import RoleModel
from typing import Optional, List
from app.db_error_handler import handle_db_error

router = fastapi.APIRouter()


@router.get("/cinematic/roles/company", tags=["users", "roles"], status_code=200)
@handle_db_error
async def get_roles_comp(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    user_company_data = users_db.get_user_company_data(user_id=user_identification.id)
    if user_company_data and (user_company_data.position == CompanyPositions.MANAGER or user_company_data.position == CompanyPositions.OWNER):
        return {"data" : db.get_company_roles(company_id=user_company_data.company_id)}
    else:
        raise fastapi.HTTPException(status_code=400, detail="you must be manager or owner to acccess company roles")


@router.get("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=200)
@handle_db_error
async def get_role_by_id(role_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    role = db.get_role_by_id(role_id=role_id)
    if role:
        user_company_data = users_db.get_user_company_data(user_id=user_identification.id)
        if user_company_data and user_company_data.company_id == role.company_id:
            if user_company_data.position == CompanyPositions.MANAGER or user_company_data.position == CompanyPositions.OWNER:
                return {"data" : role}
            else:
                raise fastapi.HTTPException(status_code=400, detail="you must be manager or owner to acccess company roles")
        else:
            raise fastapi.HTTPException(status_code=400, detail="the role you are trying to access does not belong to your company")
    else:
        raise fastapi.HTTPException(status_code=400, detail="the role you are trying to access does not exist")


@router.post("/cinematic/roles/company", tags=["users", "roles"], status_code=201)
@handle_db_error
async def upload_role(role_data : RoleModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    user_company_data = users_db.get_user_company_data(user_id=user_identification.id)
    if user_company_data and (user_company_data.position == CompanyPositions.MANAGER or user_company_data.position == CompanyPositions.OWNER):
        role_data.company_id = user_company_data.company_id
        role_data.created_by_id = user_identification.id
        db.post_role(role_data)
        return {"info" : "role succesfully posted"}
    else:
        raise fastapi.HTTPException(status_code=400, detail="you must be manager or owner to post company roles")


@router.put("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=200)
@handle_db_error
async def update_role(role_id: int, role_data : RoleModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    role = db.get_role_by_id(role_id=role_id)
    if role:
        user_company_data = users_db.get_user_company_data(user_id=user_identification.id)
        if user_company_data and user_company_data.company_id == role.company_id:
            if user_company_data.position == CompanyPositions.MANAGER or user_company_data.position == CompanyPositions.OWNER:
                role_data.id = role_id
                role_data.company_id = user_company_data.company_id
                role_data.created_by_id = None
                db.put_role(role_data)
                return {"info" : "role succesfully updated"}
            else:
                raise fastapi.HTTPException(status_code=400, detail="you must be manager or owner to edit company roles")
        else:
            raise fastapi.HTTPException(status_code=400, detail="the role you are trying to access does not belong to your company")
    else:
        raise fastapi.HTTPException(status_code=400, detail="the role you are trying to access does not exist")


@router.delete("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=204)
@handle_db_error
async def delete_role(role_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    role = db.get_role_by_id(role_id=role_id)
    if role:
        user_company_data = users_db.get_user_company_data(user_id=user_identification.id)
        if user_company_data and user_company_data.company_id == role.company_id:
            if user_company_data.position == CompanyPositions.MANAGER or user_company_data.position == CompanyPositions.OWNER:
                db.delete_role_by_id(role_id)
                return {"info" : "role succesfully deleted"}
            else:
                raise fastapi.HTTPException(status_code=400, detail="you must be manager or owner to delete company roles")
        else:
            raise fastapi.HTTPException(status_code=400, detail="the role you are trying to delete does not belong to your company")
    else:
        raise fastapi.HTTPException(status_code=400, detail="the role you are trying to delete does not exist")


# CODE REFACTOR, DO MANY FUNCTIONS THAT CHECK SOMETHING, LIKE IF THE TWO USERS WORK IN THE SAME COMPANY, etc..
# Role assignment endpoints

@router.get("/cinematic/roles/users/{user_id}", tags=["users", "roles"], status_code=200)
@handle_db_error
async def get_assigned_roles(user_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    authorized_user_company_data = users_db.get_user_company_data(user_id=user_identification.id)
    parameter_user_company_data = users_db.get_user_company_data(user_id=user_id)
    if authorized_user_company_data and (authorized_user_company_data.position == CompanyPositions.MANAGER or authorized_user_company_data.position == CompanyPositions.OWNER):
        if parameter_user_company_data and parameter_user_company_data.company_id == authorized_user_company_data.company_id:
            return {"data" : db.get_assgined_roles_by_user_id(user_id=user_id)}
        else:
            raise fastapi.HTTPException(status_code=400, detail="you are not in the same company as the provided user")
    else:
        raise fastapi.HTTPException(status_code=400, detail="you must be a manager or owner user to get assigned roles")


@router.get("/cinematic/roles/users/{role_id}", tags=["users", "roles"], status_code=200)
@handle_db_error
async def get_users_with_role(role_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Check if the authorized user is Owner or Manager and if the role_id company matches authorized user company
    # If yes get users by role
    return {}


@router.post("/cinematic/roles/users/{role_id}/{user_id}", tags=["users", "roles"], status_code=201)
@handle_db_error
async def assign_role(role_id: int, user_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Check if the authorized user is owner or manager and if both the role the user and the authorized user belong to the same company
    # If yes assign the role
    return {}