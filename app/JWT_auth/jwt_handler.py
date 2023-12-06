# JWT vs storing session ID - JWT is better, because it doesnt have to do a lookup each time and will work accross multiple servers
import jwt
from fastapi import HTTPException
import time
from decouple import config
from app.JWT_auth.user_identification import UserIdentification

_jwt_secret = config("jwt_secret")
_jwt_algorithm = config("jwt_algorithm")
_token_expire_after : int = int(config("token_expire_after"))


# This function is used for creating Json Web Token, it will encrypt user data into JWT by using JWT_SECRET
def signJWT(user_identifcation : UserIdentification) -> str:
    payload = {
        "email" : user_identifcation.email,
        "id" : user_identifcation.id,
        "iat" : time.time()
    }
    token = jwt.encode(payload=payload, key=_jwt_secret, algorithm=_jwt_algorithm)
    return token


# This function decodes JWT token into subject data, throws appropriate erros if necessary
def decodeJWT(token : str) -> UserIdentification:
    try:
        payload = jwt.decode(jwt=token, key=_jwt_secret, algorithms=_jwt_algorithm)
        if payload['iat'] + _token_expire_after >= time.time():
            return UserIdentification(id=payload["id"], email=payload["email"])
        else:
            raise jwt.ExpiredSignatureError()
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='JWT signature has expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid JWT')
    except KeyError:
        raise HTTPException(status_code=401, detail='Invalid JWT: Key error: Wrong payload')