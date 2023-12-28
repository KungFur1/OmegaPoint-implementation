import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
import app.users.roles.db as db
import app.users.db as users_db
from mysql.connector import Error as DBError
from app.users.model import CompanyPositions
from app.users.roles.model import RoleCreateModel, RoleUpdateModel, AssignedRole
from typing import Optional, List
from app.db_error_handler import handle_db_error
import app.users.check as users_check
import app.users.roles.check as check

router = fastapi.APIRouter()


@router.get("/cinematic/roles/company", tags=["users", "roles"], status_code=200)
@handle_db_error
async def get_roles_comp(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)

    users_check.is_owner_or_manager(user_company_data=auth_user_cd)
    
    return {"data" : db.get_company_roles(company_id=auth_user_cd.company_id)}


@router.get("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=200)
@handle_db_error
async def get_role_by_id(role_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    role = db.get_role_by_id(role_id=role_id)

    users_check.is_owner_or_manager(user_company_data=auth_user_cd)
    check.role_is_same_company(role=role, user_company_data=auth_user_cd)

    return {"data" : role}


@router.post("/cinematic/roles/company", tags=["users", "roles"], status_code=201)
@handle_db_error
async def upload_role(role_data : RoleCreateModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)

    users_check.is_owner_or_manager(user_company_data=auth_user_cd)
    
    role_data.company_id = auth_user_cd.company_id
    role_data.created_by_id = user_identification.id
    db.post_role(role_data)
    return {"info" : "role succesfully posted"}


@router.put("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=200)
@handle_db_error
async def update_role(role_id: int, role_update_data : RoleUpdateModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    role = db.get_role_by_id(role_id=role_id)

    users_check.is_owner_or_manager(auth_user_cd)
    check.role_is_same_company(role=role, user_company_data=auth_user_cd)

    db.put_role(role_update_data)
    return {"info" : "role succesfully updated"}


@router.delete("/cinematic/roles/company/{role_id}", tags=["users", "roles"], status_code=204)
@handle_db_error
async def delete_role(role_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    role = db.get_role_by_id(role_id=role_id)
    
    users_check.is_owner_or_manager(auth_user_cd)
    check.role_is_same_company(role=role, user_company_data=auth_user_cd)
    
    db.delete_role_by_id(role_id)
    return {"info" : "role succesfully deleted"}


# Role assignment endpoints


@router.get("/cinematic/roles/users/byuser/{user_id}", tags=["users", "roles"], status_code=200)
@handle_db_error
async def get_assigned_roles(user_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    param_user_cd = users_db.get_user_company_data(user_id=user_id)

    users_check.is_owner_or_manager(auth_user_cd)
    users_check.users_are_same_company(user1_company_data=param_user_cd, user2_company_data=auth_user_cd)
    
    return {"data" : db.get_assgined_roles_by_user_id(user_id=user_id)}


@router.get("/cinematic/roles/users/byrole/{role_id}", tags=["users", "roles"], status_code=200)
@handle_db_error
async def get_users_with_role(role_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    role = db.get_role_by_id(role_id=role_id)

    users_check.is_owner_or_manager(user_company_data=auth_user_cd)
    check.role_is_same_company(role=role, user_company_data=auth_user_cd)

    return {"data" : db.get_assgined_roles_by_role_id(role_id=role_id)}


@router.post("/cinematic/roles/users/{role_id}/{user_id}", tags=["users", "roles"], status_code=201)
@handle_db_error
async def assign_role(role_id: int, user_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    param_user_cd = users_db.get_user_company_data(user_id=user_id)
    role = db.get_role_by_id(role_id=role_id)
    
    users_check.is_owner_or_manager(user_company_data=auth_user_cd)
    users_check.users_are_same_company(user1_company_data=auth_user_cd, user2_company_data=param_user_cd)
    check.role_is_same_company(role=role, user_company_data=auth_user_cd)
    check.role_is_not_assigned(role_id=role_id, user_id=user_id)

    db.post_assigned_role(assinged_role=AssignedRole(user_id=user_id, role_id=role_id))
    return {"info" : "role succesfully assigned"}