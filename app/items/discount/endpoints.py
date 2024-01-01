import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.items.discount.model import ItemDiscountModel, ItemDiscountCreateModel
import app.items.discount.db as discount_db
from app.db_error_handler import handle_db_error
import app.users.check as users_check

router = fastapi.APIRouter()

@router.get("/cinematic/items/{item_id}/discounts", tags=["discounts"], status_code=200)
@handle_db_error
async def get_item_discounts(item_id: str, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {"data": discount_db.get_item_discounts(item_id)}


@router.post("/cinematic/items/{item_id}/discounts", tags=["discounts"], status_code=201)
@handle_db_error
async def create_item_discount(item_id: str, item_discount_data: ItemDiscountCreateModel = fastapi.Body(default=None), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    discount_db.post_item_discount(item_id, item_discount_data)
    return {"info": "item discount successfully created"}


@router.put("/cinematic/items/discounts/{discount_id}", tags=["discounts"], status_code=200)
@handle_db_error
async def edit_item_discount(discount_id: str, item_discount_data: ItemDiscountCreateModel = fastapi.Body(default=None), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    discount_db.put_item_discount(discount_id, item_discount_data)
    return {"info": "item discount successfully updated"}


@router.delete("/cinematic/items/discounts/{discount_id}", tags=["discounts"], status_code=204)
@handle_db_error
async def delete_item_discount(discount_id: str, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):    
    discount_db.delete_item_discount(discount_id)
    return {"info": "item discount successfully deleted"}