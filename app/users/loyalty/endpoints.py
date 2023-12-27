import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
import app.users.loyalty.db as db
from app.db_error_handler import handle_db_error
import app.users.check as users_check
from app.users.loyalty.model import LoyaltCreateModel

router = fastapi.APIRouter()


@router.get("/cinematic/loyalty", tags=["loyalty"], status_code=200)
@handle_db_error
async def get_loyalty(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {"data" : "Not implemented."}


@router.get("/cinematic/loyalty/{id}", tags=["loyalty"], status_code=200)
@handle_db_error
async def get_loyalty_by_id(id : int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {"data" : "Not implemented."}


@router.post("/cinematic/loyalty", tags=["loyalty"], status_code=201)
@handle_db_error
async def create_loyalty(loyalty_create_data : LoyaltCreateModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {"data" : "Not implemented."}


@router.delete("/cinematic/loyalty/{id}", tags=["loyalty"], status_code=204)
@handle_db_error
async def delete_loyalty(id : int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {"data" : "Not implemented."}