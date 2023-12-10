# Authorization - is making sure that the user that sends requests to your server is the same user that loged in
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.JWT_auth.jwt_handler import decodeJWT
from app.JWT_auth.user_identification import UserIdentification, CompleteUserInformation
from mysql.connector import Error as DBError
import app.users.db as users_db
from app.users.roles.access_handler import AccessModel, get_user_access
from app.users.model import UserCompanyDataModel

_security = HTTPBearer()


# Use this function in any endpoint to get access to authorized user information
def authorization_wrapper(auth : HTTPAuthorizationCredentials = Security(_security)) -> UserIdentification:
    return decodeJWT(auth.credentials)


# Pass authorized user id to this function to get complete information about user, returns None in case of database error 
def get_complete_user_information(user_id: int) -> CompleteUserInformation:
    try:
        regular_user_data = users_db.get_user_regular_data(user_id=user_id)
        company_user_data = users_db.get_user_company_data(user_id=user_id)
        access_user_data : AccessModel
        if company_user_data:
            access_user_data = get_user_access(user_id=user_id)
        else:
            company_user_data = UserCompanyDataModel(user_id=None, company_id=None, position=None)
            access_user_data = None
        complete_user_information = CompleteUserInformation(id=regular_user_data.id, email=regular_user_data.email, company_id=company_user_data.company_id, 
                                                            position=company_user_data.position, access=access_user_data, created_at=regular_user_data.created_at, 
                                                            phone_number=regular_user_data.phone_number, first_name=regular_user_data.first_name, 
                                                            last_name=regular_user_data.last_name, address=regular_user_data.address)
        return complete_user_information
    except DBError:
        return None