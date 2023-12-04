import fastapi
from app.users.user_model import UserSchema, UserLoginSchema
from app.JWT_auth.authentication import get_password_hash, verify_password
from app.JWT_auth.jwt_handler import signJWT
from app.database import users

router = fastapi.APIRouter()


# User registration # Currently not checking if there already is such user
@router.post("/user/register", tags=["user"], status_code=201)
async def user_register(user : UserSchema = fastapi.Body(default=None)):
    user.password = get_password_hash(user.password) # Encrypt the password
    users.append(user.model_dump()) # save in the database; model_dump() turns object into a dictionary
    return {"info": "success"}


# User login
@router.post("/user/login", tags=["user"], status_code=201)
async def user_login(user_login_schema : UserLoginSchema = fastapi.Body(default=None)):
    user = None # First find if user with this email exists
    for x in users:
        if x["email"] == user_login_schema.email:
            user = x
            break
    # Then check if the passwords match
    if (user is None) or (not verify_password(user_login_schema.password, user["password"])):
        raise fastapi.HTTPException(status_code=401, detail="Invalid email and/or password")
    token = signJWT(user["email"]) # Encrypt the token
    return {'token': token}
