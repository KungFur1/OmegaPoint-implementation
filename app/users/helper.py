import fastapi
from app.users.model import UserModel, UserLoginModel, UserAuthenticationDataModel
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authentication import get_password_hash, verify_password
from app.JWT_auth.jwt_handler import signJWT
import app.users.db as db
from mysql.connector import Error as DBError


# USER REGISTER AND LOGIN FUNCTIONS:

# Register the user with basic checks
def register(user_data : UserModel):
    try:
        if db.get_user_by_email(email=user_data.email):
            raise fastapi.HTTPException(status_code=400, detail="user with such email already exists")
        user_data.password = get_password_hash(user_data.password)
        db.post_user(user_data)
        return {"info" : "registration succesful"}
    except DBError as e:
        raise fastapi.HTTPException(status_code=500, detail="database error")
    

# Login with some basic checks
def login(login_data : UserLoginModel):
    try:
        x : UserAuthenticationDataModel = db.get_user_by_email(login_data.email)
        if x and verify_password(login_data.password, x.password):
            return {"token" : signJWT(UserIdentification(id=x.id, email=x.email))}
        else:
            raise fastapi.HTTPException(status_code=400, detail="bad password and/or email")
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")
