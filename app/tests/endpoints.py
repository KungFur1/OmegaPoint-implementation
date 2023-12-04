import fastapi
from app.JWT_auth.auth import AuthHandler

router = fastapi.APIRouter()

# TEST PROTECTED ROUTE:
@router.get('/protected-route', tags=["test"])
async def protected_route(email : str = fastapi.Depends(AuthHandler.authorization_wrapper)):
    return {"data" : "Hello, your email is: " + email}


# TEST UNPROTECTED ROUTE:
@router.get('/', tags=["test"])
async def root():
    return {"data" : "Hello, this the root URL"}
