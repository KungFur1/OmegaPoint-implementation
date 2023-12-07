import fastapi
from app.users.model import UserModel, UserLoginModel, UserAuthenticationDataModel
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authentication import get_password_hash, verify_password
from app.JWT_auth.jwt_handler import signJWT
import app.users.db as db

# BASE USER REGISTER AND LOGIN FUNCTIONS:

# Register the user with basic checks
def register(user_data : UserModel):
    if db.get_user_by_email(email=user_data.email):
        raise fastapi.HTTPException(status_code=400, detail="user with such email already exists")
    user_data.password = get_password_hash(user_data.password)
    if db.post_user(user_data):
        return {"info" : "registration succesful"}
    else:
        raise fastapi.HTTPException(status_code=500, detail="failed to upload registration data to database")
    

# Login with some basic checks
def login(login_data : UserLoginModel):
    x : UserAuthenticationDataModel = db.get_user_by_email(login_data.email)
    if x and verify_password(login_data.password, x.password):
        return {"token" : signJWT(UserIdentification(id=x.id, email=x.email))}
    else:
        raise fastapi.HTTPException(status_code=400, detail="bad password and/or email")
