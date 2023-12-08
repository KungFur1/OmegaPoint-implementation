import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authentication import get_password_hash, verify_password
from app.JWT_auth.jwt_handler import signJWT
from app.users.model import UserModel, UserLoginModel, UserAuthenticationDataModel
import app.users.db as db
from mysql.connector import Error as DBError


# ! Company fields must be None if this is not a company user
def register(user_data : UserModel):
    try:
        if db.get_user_authentication_data_by_email(email=user_data.email):
            raise fastapi.HTTPException(status_code=400, detail="user with such email already exists")
        user_data.password = get_password_hash(user_data.password)
        if user_data.company_id:
            db.post_company_user(user_data)
        else:
            db.post_user(user_data)
        return {"info" : "registration succesful"}
    except DBError as e:
        raise fastapi.HTTPException(status_code=500, detail="database error")
    

def login(login_data : UserLoginModel):
    try:
        x : UserAuthenticationDataModel = db.get_user_authentication_data_by_email(login_data.email)
        if x and verify_password(login_data.password, x.password):
            return {"token" : signJWT(UserIdentification(id=x.id, email=x.email))}
        else:
            raise fastapi.HTTPException(status_code=400, detail="bad password and/or email")
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")
