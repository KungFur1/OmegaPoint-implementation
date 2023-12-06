# Authorization - is making sure that the user that sends requests to your server is the same user that loged in
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.JWT_auth.jwt_handler import decodeJWT
from app.JWT_auth.user_identification import UserIdentification

_security = HTTPBearer()


# Use this function in any endpoint to get access to authorized user information
def authorization_wrapper(auth : HTTPAuthorizationCredentials = Security(_security)) -> UserIdentification:
    return decodeJWT(auth.credentials)
