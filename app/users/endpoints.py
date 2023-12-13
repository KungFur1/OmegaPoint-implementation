import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.users.model import UserRegisterModel, UserLoginModel, CompanyPositions, UserAuthenticationDataModel
import app.users.db as db
import app.company.db as company_db
from mysql.connector import Error as DBError
import app.users.logreg as logreg
from app.db_error_handler import handle_db_error
import app.users.check as check
import app.company.check as company_check

router = fastapi.APIRouter()


# AUTHENTICATION START

# Register a regular user
@router.post("/cinematic/users/register", tags=["regular_users", "register"], status_code=201)
@handle_db_error
async def user_register(new_user : UserRegisterModel = fastapi.Body(default=None)):
    new_user.company_id = None
    new_user.position = None
    return logreg.register(new_user)


# Login for all users
@router.post("/cinematic/users/login", tags=["regular_users", "login"], status_code=201)
@handle_db_error
async def user_login(login_data : UserLoginModel = fastapi.Body(default=None)):
    return logreg.login(login_data)


# Register a company owner user, done by the system administrators only
@router.post("/cinematic/users/company/owner/register", tags=["company_users", "register", "owners"], status_code=201)
@handle_db_error
async def owner_register(new_owner : UserRegisterModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    check.is_admin(user_id=user_identification.id)
    company_check.company_exists(company_id=new_owner.company_id)
    
    new_owner.company_id = new_owner.company_id
    new_owner.position = CompanyPositions.OWNER
    return logreg.register(new_owner)


# Register a company manager user, done by the company owner users only
@router.post("/cinematic/users/company/manager/register", tags=["company_users", "register", "owners", "managers"], status_code=201)
@handle_db_error
async def manager_register(new_manager : UserRegisterModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = db.get_user_company_data(user_id=user_identification.id)

    check.is_owner(user_company_data=auth_user_cd)
    
    new_manager.company_id = auth_user_cd.company_id
    new_manager.position = CompanyPositions.MANAGER
    return logreg.register(new_manager)


# Register a company employee user, done by the company manager users and company owner users only
@router.post("/cinematic/users/company/employee/register", tags=["company_users", "register", "owners", "managers", "employees"], status_code=201)
@handle_db_error
async def employee_register(new_employee : UserRegisterModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    auth_user_cd = db.get_user_company_data(user_id=user_identification.id)

    check.is_owner_or_manager(user_company_data=auth_user_cd)
    
    new_employee.company_id = auth_user_cd.company_id
    new_employee.position = CompanyPositions.EMPLOYEE
    return logreg.register(new_employee)


# AUTHENTICATION END



# ENDPOINTS FOR COMPANY MANAGERS/OWNERS FOR MANAGING COMPANY USERS

# Get all company users
@router.get("/cinematic/users/company", tags=["company_users", "managers", "owners"], status_code=200)
@handle_db_error
async def get_all_company_users(user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# Get a specific user from the company 
@router.get("/cinematic/users/company/{user_id}", tags=["company_users", "managers", "owners"], status_code=200)
@handle_db_error
async def get_user_by_id(user_id: int, user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# Update company employee (EXCEPT Owner/Manager), Owner can update any user
@router.put("/cinematic/users/company/{user_id}", tags=["company_users", "managers", "owners"], status_code=200)
@handle_db_error
async def update_company_user(user_id: int, employee_data : UserRegisterModel = fastapi.Body(default=None), user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# Delete user, that was created by that company (EXCEPT Owner/Manager), Owner can delete any user
@router.delete("/cinematic/users/company/{user_id}", tags=["company_users", "managers", "owners"], status_code=204)
@handle_db_error
async def delete_company_user(user_id: int, user_identification = fastapi.Depends(authorization_wrapper)):
    return {}
