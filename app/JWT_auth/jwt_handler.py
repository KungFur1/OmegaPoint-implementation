# JWT vs storing session ID - JWT is better, because it doesnt have to do a lookup each time and will work accross multiple servers
import jwt
from fastapi import HTTPException
import time
from decouple import config

_jwt_secret = config("jwt_secret")
_jwt_algorithm = config("jwt_algorithm")
_token_expire_after : int = int(config("token_expire_after"))


# This function is used for creating Json Web Token, it will encrypt user data into JWT by using JWT_SECRET
def signJWT(user_identifcation : str) -> str:
    payload = {
        "sub" : user_identifcation,
        "iat" : time.time()
    }
    token = jwt.encode(payload=payload, key=_jwt_secret, algorithm=_jwt_algorithm)
    return token


# This function decodes JWT token into subject data, throws appropriate erros if necessary
def decodeJWT(token : str) -> str:
    try:
        payload = jwt.decode(jwt=token, key=_jwt_secret, algorithms=_jwt_algorithm)
        if payload['iat'] + _token_expire_after >= time.time():
            return payload["sub"]
        else:
            raise jwt.ExpiredSignatureError()
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='JWT signature has expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid JWT')