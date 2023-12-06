import fastapi
from app.JWT_auth.authorization import authorization_wrapper
# from app.users.users_db import get_users, insert_user
# from app.users.user_model import UserSchema

router = fastapi.APIRouter()

# TEST PROTECTED ROUTE:
@router.get('/protected-route', tags=["test"])
async def protected_route(email : str = fastapi.Depends(authorization_wrapper)):
    return {"data" : "Hello, your email is: " + email}


# TEST UNPROTECTED ROUTE:
@router.get('/', tags=["test"])
async def root():
    return {"data" : "Hello, this the root URL"}


# # TEST SELECT ALL USERS FROM DB:
# @router.get('/select-users', tags=["test"])
# async def select_users():
#     return get_users()


# # TEST POST USER TO DB:
# @router.post('/post-user', tags=["test"])
# async def post_user(user : UserSchema):
#     status = insert_user(user)
#     if status:
#         return {"info": "success"}
#     else:
#         return {"info": "failed to post user"}