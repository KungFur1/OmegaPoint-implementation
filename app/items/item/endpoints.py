import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.items.item.model import ItemCreateModel, ItemUpdateModel
import app.items.item.db as item_db
from app.db_error_handler import handle_db_error
import app.users.check as users_check

router = fastapi.APIRouter()


@router.get("/cinematic/items", tags=["items"], status_code=200)
@handle_db_error
async def get_all_items(user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {"data": item_db.get_all_items()}


@router.get("/cinematic/items/{item_id}", tags=["items"], status_code=200)
@handle_db_error
async def get_item_by_id(item_id: str, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    return {"data": item_db.get_item_by_id(item_id=item_id)}


@router.post("/cinematic/items", tags=["items"], status_code=201)
@handle_db_error
async def create_item(item_create_data: ItemCreateModel = fastapi.Body(default=None), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    # users_check.is_admin(user_id=user_identification.id)
    item_db.post_item(item_create_data)
    return {"info": "item successfully inserted"}


@router.put("/cinematic/items/{item_id}", tags=["items"], status_code=200)
@handle_db_error
async def edit_item(item_id: str, item_update_data: ItemUpdateModel = fastapi.Body(default=None), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    # users_check.is_admin(user_id=user_identification.id)
    item_db.put_item(item_id, item_update_data)
    return {"info": "item successfully updated"}


@router.delete("/cinematic/items/{item_id}", tags=["items"], status_code=204)
@handle_db_error
async def delete_item(item_id: str, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    # users_check.is_admin(user_id=user_identification.id)
    item_db.delete_item(item_id)
    return {"info": "item successfully deleted"}


