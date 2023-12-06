import fastapi
from app.JWT_auth.authentication import get_password_hash, verify_password
from app.JWT_auth.jwt_handler import signJWT
from app.JWT_auth.authorization import UserIdentification
from app.users.model import UserModel, UserLoginModel, CompanyPositions, UserAuthenticationDataModel
import app.users.db as db

router = fastapi.APIRouter()


# REGULAR USER AUTHENTICATION START

# Register a regular user
@router.post("/cinematic/users/register", tags=["regular_users", "register"], status_code=201)
async def user_register(user_data : UserModel = fastapi.Body(default=None)):
    if db.email_exists(email=user_data.email):
        raise fastapi.HTTPException(status_code=400, detail="user with such email already exists")
    user_data.password = get_password_hash(user_data.password)
    if db.insert_user_to_database(user_data):
        return {"info" : "registration succesful"}
    else:
        raise fastapi.HTTPException(status_code=500, detail="failed to upload registration data to database")


# Login for regular users
@router.post("/cinematic/users/login", tags=["regular_users", "login"], status_code=201)
async def user_login(login_data : UserLoginModel = fastapi.Body(default=None)):
    x : UserAuthenticationDataModel = db.retrieve_user_by_email(login_data.email)
    if x and verify_password(login_data.password, x.password):
        return {"token" : signJWT(UserIdentification(id=x.id, email=x.email))}
    else:
        raise fastapi.HTTPException(status_code=400, detail="bad password and/or email")

# REGULAR USER AUTHENTICATION END





# COMPANY USER AUTHENTICATION START

# Register a company owner user, done by the system administrators only
@router.post("/cinematic/company/users/owner/register", tags=["company_users", "register", "owners"], status_code=201)
async def owner_register(owner_data : UserModel = fastapi.Body(default=None)):
    return {}


# Register a company manager user, done by the company owner user only
@router.post("/cinematic/company/users/manager/register", tags=["company_users", "register", "owners", "managers"], status_code=201)
async def manager_register(manager_data : UserModel = fastapi.Body(default=None)):
    return {}


# Register a company employee user, done by the company manager users and company owner user only
@router.post("/cinematic/company/users/employee/register", tags=["company_users", "register", "owners", "managers", "employees"], status_code=201)
async def employee_register(employee_data : UserModel = fastapi.Body(default=None)):
    return {}


# Login for users that belong to some company
@router.post("/cinematic/company/users/login", tags=["company_users", "login", "owners", "managers", "employees"], status_code=201)
async def company_user_login(login_data : UserLoginModel = fastapi.Body(default=None), status_code=201):
    return {}

# COMPANY USER AUTHENTICATION END


# ENDPOINTS FOR COMPANY MANAGERS/OWNERS FOR MANAGING COMPANY USERS

# Get all company users
@router.get("/cinematic/company/users", tags=["company_users", "managers", "owners"])
async def get_all_company_users():
    return {}


# Get a specific user from the company 
@router.get("/cinematic/company/{user_id}", tags=["company_users", "managers", "owners"])
async def get_user_by_id():
    return {}


# Update company employee (EXCEPT Owner/Manager), Owner can update any user
@router.put("/cinematic/company/{user_id}", tags=["company_users", "managers", "owners"])
async def update_company_user():
    return {}


# Delete user, that was created by that company (EXCEPT Owner/Manager), Owner can delete any user
@router.delete("/cinematic/company/{user_id}", tags=["company_users", "managers", "owners"])
async def delete_company_user():
    return {}


# ROLE MANAGMENT ENDPOINTS (MAYBE THIS SHOULD BE ANOTHER COMPONENT OR FOLDER?)


# LOYALTY MANAGMENT ENDPOINTS ???

