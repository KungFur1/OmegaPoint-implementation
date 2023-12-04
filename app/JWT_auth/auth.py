# Authentication - take username and password and authenticate if username and password is correct.
# Authorization - is making sure that the user that sends requests to your server is the same user that loged in.
# JWT vs storing session ID - JWT is better, because it doesnt have to do a lookup each time and will work accross multiple servers.

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
import time
from decouple import config


class AuthHandler():
    security = HTTPBearer()
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Password encrypting object
    jwt_secret = config("jwt_secret")
    jwt_algorithm = config("jwt_algorithm")
    token_expire_after : int = int(config("token_expire_after"))

    # Returns an encrypted version of the password
    @staticmethod
    def get_password_hash(password):
        return AuthHandler.password_context.hash(password)
    
    # Returns a boolean if the passwords match
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return AuthHandler.password_context.verify(plain_password, hashed_password)
    

    # This function is used for creating Json Web Token, it will encrypt user data into JWT by using JWT_SECRET
    @staticmethod
    def signJWT(user_identifcation : str):
        payload = {
            "sub" : user_identifcation,
            "iat" : time.time()
        }
        token = jwt.encode(payload=payload, key=AuthHandler.jwt_secret, algorithm=AuthHandler.jwt_algorithm)
        return token
    

    # This function decodes JWT token into user data
    @staticmethod
    def decodeJWT(token : str):
        try:
            payload = jwt.decode(jwt=token, key=AuthHandler.jwt_secret, algorithms=AuthHandler.jwt_algorithm)
            return payload["sub"] if payload['iat'] + AuthHandler.token_expire_after >= time.time() else None
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='JWT signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')
        

    @staticmethod
    def authorization_wrapper(auth : HTTPAuthorizationCredentials = Security(security)):
        return AuthHandler.decodeJWT(auth.credentials)
    