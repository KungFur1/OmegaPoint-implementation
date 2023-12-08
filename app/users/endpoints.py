# {"data" : data} - when returning some data
# {"info" : success_message} - when some operation was successful
# raise fastapi.HTTPException - when something is wrong, provide detail
# all messages should start with non-capital letter and end without a dot
import fastapi
from app.JWT_auth.user_identification import UserIdentification # Authorization!
from app.JWT_auth.authorization import authorization_wrapper # Authorization!
from app.JWT_auth.authentication import get_password_hash, verify_password
from app.JWT_auth.jwt_handler import signJWT
from app.users.model import UserModel, UserLoginModel, CompanyPositions, UserAuthenticationDataModel
import app.users.db as db
import app.company.db as company_db
from mysql.connector import Error as DBError

router = fastapi.APIRouter()


# TEST PROTECTED ROUTE:
@router.get('/protected-route', tags=["test"])
async def protected_route(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {"data" : "Hello, your email is: " + user_identification.email + " Your ID: " + str(user_identification.id)}


# TEST UNPROTECTED ROUTE:
@router.get('/', tags=["test"])
async def root():
    return {"data" : "Hello, this the root URL"}




# REGULAR USER AUTHENTICATION START

# Register a regular user
@router.post("/cinematic/users/register", tags=["regular_users", "register"], status_code=201)
async def user_register(user_data : UserModel = fastapi.Body(default=None)):
    try:
        if db.get_user_by_email(email=user_data.email):
            raise fastapi.HTTPException(status_code=400, detail="user with such email already exists")
        user_data.password = get_password_hash(user_data.password)
        db.post_user(user_data)
        return {"info" : "registration succesful"}
    except DBError as e:
        raise fastapi.HTTPException(status_code=500, detail="database error")


# Login for regular users
@router.post("/cinematic/users/login", tags=["regular_users", "login"], status_code=201)
async def user_login(login_data : UserLoginModel = fastapi.Body(default=None)):
    try:
        x : UserAuthenticationDataModel = db.get_user_by_email(login_data.email)
        if x and verify_password(login_data.password, x.password):
            return {"token" : signJWT(UserIdentification(id=x.id, email=x.email))}
        else:
            raise fastapi.HTTPException(status_code=400, detail="bad password and/or email")
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")

# REGULAR USER AUTHENTICATION END





# COMPANY USER AUTHENTICATION START

# Register a company owner user, done by the system administrators only
@router.post("/cinematic/company/users/owner/register", tags=["company_users", "register", "owners"], status_code=201)
async def owner_register(owner_data : UserModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    try:
        if db.get_admin_information(user_id=user_identification.id):
            owner_data.position = CompanyPositions.OWNER
            if company_db.get_company_by_id(owner_data.company_id):
                db.post_company_user(owner_data)
                return {"info" : "owner user succesfully registered"}
            else:
                raise fastapi.HTTPException(status_code=400, detail="company with provided id does not exist")
        else:
            raise fastapi.HTTPException(status_code=400, detail="you must be admin user to register owner")
    except DBError as e:
        raise fastapi.HTTPException(status_code=500, detail="database error")


# Register a company manager user, done by the company owner user only
@router.post("/cinematic/company/users/manager/register", tags=["company_users", "register", "owners", "managers"], status_code=201)
async def manager_register(manager_data : UserModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {}


# Register a company employee user, done by the company manager users and company owner user only
@router.post("/cinematic/company/users/employee/register", tags=["company_users", "register", "owners", "managers", "employees"], status_code=201)
async def employee_register(employee_data : UserModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {}


# Login for users that belong to some company (The same as regular user login)
@router.post("/cinematic/company/users/login", tags=["company_users", "login", "owners", "managers", "employees"], status_code=201)
async def company_user_login(login_data : UserLoginModel = fastapi.Body(default=None), status_code=201):
    return {}

# COMPANY USER AUTHENTICATION END


# ENDPOINTS FOR COMPANY MANAGERS/OWNERS FOR MANAGING COMPANY USERS

# Get all company users
@router.get("/cinematic/company/users", tags=["company_users", "managers", "owners"])
async def get_all_company_users(user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# Get a specific user from the company 
@router.get("/cinematic/company/{user_id}", tags=["company_users", "managers", "owners"])
async def get_user_by_id(user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# Update company employee (EXCEPT Owner/Manager), Owner can update any user
@router.put("/cinematic/company/{user_id}", tags=["company_users", "managers", "owners"])
async def update_company_user(user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# Delete user, that was created by that company (EXCEPT Owner/Manager), Owner can delete any user
@router.delete("/cinematic/company/{user_id}", tags=["company_users", "managers", "owners"])
async def delete_company_user(user_identification = fastapi.Depends(authorization_wrapper)):
    return {}


# ROLE MANAGMENT ENDPOINTS (MAYBE THIS SHOULD BE ANOTHER COMPONENT OR FOLDER?)


# LOYALTY MANAGMENT ENDPOINTS ???

