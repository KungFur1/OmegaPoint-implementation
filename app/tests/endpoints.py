import fastapi
from app.JWT_auth.authorization import authorization_wrapper
from app.JWT_auth.authorization import UserIdentification
# from app.users.users_db import get_users, insert_user
# from app.users.user_model import UserSchema

router = fastapi.APIRouter()

# TEST PROTECTED ROUTE:
@router.get('/protected-route', tags=["test"])
async def protected_route(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {"data" : "Hello, your email is: " + user_identification.email + " Your ID: " + str(user_identification.id)}


# TEST UNPROTECTED ROUTE:
@router.get('/', tags=["test"])
async def root():
    return {"data" : "Hello, this the root URL"}
