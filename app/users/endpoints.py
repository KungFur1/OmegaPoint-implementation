import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.users.model import UserRegisterModel, UserLoginModel, CompanyPositions, UserUpdateModel
import app.users.db as db
import app.users.logreg as logreg
from app.db_error_handler import handle_db_error
import app.users.check as check
import app.company.check as company_check

router = fastapi.APIRouter()


# Authentication endpoints:


@router.post("/cinematic/users/register", tags=["regular_users", "register"], status_code=201)
@handle_db_error
async def user_register(new_user : UserRegisterModel = fastapi.Body(default=None)):
    new_user.company_id = None
    new_user.position = None
    return logreg.register(new_user)


@router.post("/cinematic/users/login", tags=["regular_users", "login"], status_code=201)
@handle_db_error
async def user_login(login_data : UserLoginModel = fastapi.Body(default=None)):
    return logreg.login(login_data)


@router.post("/cinematic/users/company/owner/register", tags=["company_users", "register", "owners"], status_code=201)
@handle_db_error
async def owner_register(new_owner : UserRegisterModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    check.is_admin(user_id=user_identification.id)
    company_check.company_exists(company_id=new_owner.company_id)
    
    new_owner.company_id = new_owner.company_id
    new_owner.position = CompanyPositions.OWNER
    return logreg.register(new_owner)


@router.post("/cinematic/users/company/manager/register", tags=["company_users", "register", "owners", "managers"], status_code=201)
@handle_db_error
async def manager_register(new_manager : UserRegisterModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = db.get_user_company_data(user_id=user_identification.id)

    check.is_owner(user_company_data=auth_user_cd)
    
    new_manager.company_id = auth_user_cd.company_id
    new_manager.position = CompanyPositions.MANAGER
    return logreg.register(new_manager)


@router.post("/cinematic/users/company/employee/register", tags=["company_users", "register", "owners", "managers", "employees"], status_code=201)
@handle_db_error
async def employee_register(new_employee : UserRegisterModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = db.get_user_company_data(user_id=user_identification.id)

    check.is_owner_or_manager(user_company_data=auth_user_cd)
    
    new_employee.company_id = auth_user_cd.company_id
    new_employee.position = CompanyPositions.EMPLOYEE
    return logreg.register(new_employee)


# Company user managment endpoints:
# Look in to this after completing everything else:
# For some reason roles [] doesnt update after assgning a role, I need to restart the server for it to update, very weird error, not sure why.
# Maybe the sql query response is cached somewhere, but that seems weird.
# Anyways I should move away from queries that merge few tables and instead merge them inside python.


@router.get("/cinematic/users/company", tags=["company_users", "managers", "owners"], status_code=200)
@handle_db_error
async def get_all_company_users(user_identification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = db.get_user_company_data(user_id=user_identification.id)

    check.is_owner_or_manager(user_company_data=auth_user_cd)

    return {"data" : db.get_users_by_company(company_id=auth_user_cd.company_id)}


@router.get("/cinematic/users/company/{user_id}", tags=["company_users", "managers", "owners"], status_code=200)
@handle_db_error
async def get_user_by_id(user_id: int, user_identification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = db.get_user_company_data(user_id=user_identification.id)
    param_user_cd = db.get_user_company_data(user_id=user_id)

    check.is_owner_or_manager(user_company_data=auth_user_cd)
    check.users_are_same_company(user1_company_data=param_user_cd, user2_company_data=auth_user_cd)

    return {"data" : db.get_company_user_by_id(user_id=user_id)}


@router.put("/cinematic/users/company/{user_id}", tags=["company_users", "managers", "owners"], status_code=200)
@handle_db_error
async def update_company_user(user_id: int, user_update_data : UserUpdateModel = fastapi.Body(default=None), user_identification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = db.get_user_company_data(user_id=user_identification.id)
    param_user_cd = db.get_user_company_data(user_id=user_id)

    check.is_owner_or_manager(user_company_data=auth_user_cd)
    check.users_are_same_company(user1_company_data=param_user_cd, user2_company_data=auth_user_cd)
    check.if_manager_then_employee(manager=auth_user_cd, employee=param_user_cd)

    db.put_user(user_id=user_id, user_data=user_update_data)
    return {"info" : "user updated successfully"}


@router.delete("/cinematic/users/company/{user_id}", tags=["company_users", "managers", "owners"], status_code=204)
@handle_db_error
async def delete_company_user(user_id: int, user_identification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = db.get_user_company_data(user_id=user_identification.id)
    param_user_cd = db.get_user_company_data(user_id=user_id)

    check.is_owner_or_manager(user_company_data=auth_user_cd)
    check.users_are_same_company(user1_company_data=param_user_cd, user2_company_data=auth_user_cd)
    check.if_manager_then_employee(manager=auth_user_cd, employee=param_user_cd)

    db.delete_user(user_id=user_id)
    return {"info" : "user deleted successfully"}
