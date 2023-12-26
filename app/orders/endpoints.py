import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
from app.orders.model import OrderPostModel
import app.orders.db as db
from app.db_error_handler import handle_db_error

router = fastapi.APIRouter()

@router.post("/cinematic/orders", tags=["orders"], status_code=201)
@handle_db_error
async def create_order(new_order : OrderPostModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.post_order(new_order)

@router.get("/cinematic/orders", tags=["orders"], status_code=200)
@handle_db_error
async def get_orders(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.get_orders(user_identification.id)