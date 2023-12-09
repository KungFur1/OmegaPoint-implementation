# Roles CRUD is only accessible to managers and owners of the company.
import fastapi
from app.JWT_auth.user_identification import UserIdentification # Authorization!
from app.JWT_auth.authorization import authorization_wrapper # Authorization!
import app.users.roles.db as db
import app.users.db as users_db
from mysql.connector import Error as DBError
from app.users.model import CompanyPositions
from app.users.roles.model import RoleModel
from typing import Optional, List

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
    try:
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
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")


@router.post("/cinematic/roles/company", tags=["users", "roles"], status_code=201)
async def upload_role(role_data : RoleModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    try:
        user_company_data = users_db.get_user_company_data(user_id=user_identification.id)
        if user_company_data and (user_company_data.position == CompanyPositions.MANAGER or user_company_data.position == CompanyPositions.OWNER):
            role_data.company_id = user_company_data.company_id
            role_data.created_by_id = user_identification.id
            db.post_role(role_data)
            return {"info" : "role succesfully posted"}
        else:
            raise fastapi.HTTPException(status_code=400, detail="you must be manager or owner to post company roles")
    except DBError as e:
        print(f"Error: {e}")
        raise fastapi.HTTPException(status_code=500, detail="database error")


@router.put("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=200)
async def update_role(role_id: int, role_data : RoleModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    try:
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
    except DBError as e:
        print(f"Error: {e}")
        raise fastapi.HTTPException(status_code=500, detail="database error")


@router.delete("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=204)
async def delete_role(role_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    # Retrieve the role`s company_id
    # Check if user is owner or manager, check if user belongs to that company.
    # If user is, delete the role
    try:
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
    except DBError as e:
        print(f"Error {e}")
        raise fastapi.HTTPException(status_code=500, detail="database error")
