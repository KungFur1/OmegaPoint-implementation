import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.users.model import UserModel, UserLoginModel, CompanyPositions, UserAuthenticationDataModel
import app.users.db as db
import app.company.db as company_db
from mysql.connector import Error as DBError
import app.users.logreg as logreg

router = fastapi.APIRouter()


# AUTHENTICATION START

# Register a regular user
@router.post("/cinematic/users/register", tags=["regular_users", "register"], status_code=201)
async def user_register(user_data : UserModel = fastapi.Body(default=None)):
    user_data.company_id = None
    user_data.position = None
    user_data.roles = None
    return logreg.register(user_data)


# Login for all users
@router.post("/cinematic/users/login", tags=["regular_users", "login"], status_code=201)
async def user_login(login_data : UserLoginModel = fastapi.Body(default=None)):
    return logreg.login(login_data)


# Register a company owner user, done by the system administrators only
@router.post("/cinematic/users/company/owner/register", tags=["company_users", "register", "owners"], status_code=201)
async def owner_register(owner_data : UserModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    try:
        if db.get_admin_information_by_id(user_id=user_identification.id):
            if company_db.get_company_by_id(owner_data.company_id):
                owner_data.company_id = owner_data.company_id
                owner_data.position = CompanyPositions.OWNER
                owner_data.roles = None
                return logreg.register(owner_data)
            else:
                raise fastapi.HTTPException(status_code=400, detail="company with provided id does not exist")
        else:
            raise fastapi.HTTPException(status_code=400, detail="you must be admin user to register owner")
    except DBError as e:
        raise fastapi.HTTPException(status_code=500, detail="database error")


# Register a company manager user, done by the company owner users only
@router.post("/cinematic/users/company/manager/register", tags=["company_users", "register", "owners", "managers"], status_code=201)
async def manager_register(manager_data : UserModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    try:
        company_data = db.get_user_company_data(user_id=user_identification.id)
        if company_data and company_data.position == CompanyPositions.OWNER:
            manager_data.company_id = company_data.company_id
            manager_data.position = CompanyPositions.MANAGER
            manager_data.roles = None
            return logreg.register(manager_data)
        else:
            raise fastapi.HTTPException(status_code=400, detail="you must be owner user to register manager user")
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")


# Register a company employee user, done by the company manager users and company owner users only
@router.post("/cinematic/users/company/employee/register", tags=["company_users", "register", "owners", "managers", "employees"], status_code=201)
async def employee_register(employee_data : UserModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    try:
        company_data = db.get_user_company_data(user_id=user_identification.id)
        if company_data and (company_data.position == CompanyPositions.OWNER or company_data.position == CompanyPositions.MANAGER):
            employee_data.company_id = company_data.company_id
            employee_data.position = CompanyPositions.EMPLOYEE
            employee_data.roles = None
            return logreg.register(employee_data)
        else:
            raise fastapi.HTTPException(status_code=400, detail="you must be owner user to register manager user")
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")


# AUTHENTICATION END



# ENDPOINTS FOR COMPANY MANAGERS/OWNERS FOR MANAGING COMPANY USERS

# Get all company users
@router.get("/cinematic/users/company", tags=["company_users", "managers", "owners"], status_code=200)
async def get_all_company_users(user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# Get a specific user from the company 
@router.get("/cinematic/users/company/{user_id}", tags=["company_users", "managers", "owners"], status_code=200)
async def get_user_by_id(user_id: int, user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# Update company employee (EXCEPT Owner/Manager), Owner can update any user
@router.put("/cinematic/users/company/{user_id}", tags=["company_users", "managers", "owners"], status_code=200)
async def update_company_user(user_id: int, employee_data : UserModel = fastapi.Body(default=None), user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# Delete user, that was created by that company (EXCEPT Owner/Manager), Owner can delete any user
@router.delete("/cinematic/users/company/{user_id}", tags=["company_users", "managers", "owners"], status_code=204)
async def delete_company_user(user_id: int, user_identification = fastapi.Depends(authorization_wrapper)):
    return {}

