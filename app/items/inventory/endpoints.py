import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.items.inventory.model import InventoryModel, InventoryCreateModel, InventoryUpdateModel
import app.items.inventory.db as inventory_db
from app.db_error_handler import handle_db_error
import app.users.check as users_check

router = fastapi.APIRouter()


@router.get("/cinematic/inventory", tags=["inventory"], status_code=200)
@handle_db_error
async def get_all_inventory():
    return {"data": inventory_db.get_all_inventory()}


@router.get("/cinematic/inventory/{inventory_id}", tags=["inventory"], status_code=200)
@handle_db_error
async def get_inventory_by_id(inventory_id: str):
    return {"data": inventory_db.get_inventory_by_id(inventory_id=inventory_id)}


@router.post("/cinematic/inventory", tags=["inventory"], status_code=201)
@handle_db_error
async def create_inventory(inventory_create_data: InventoryCreateModel = fastapi.Body(default=None),
                            user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):

    inventory_db.post_inventory(inventory_create_data=inventory_create_data)
    return {"info": "inventory successfully created"}


@router.put("/cinematic/inventory/{inventory_id}", tags=["inventory"], status_code=200)
@handle_db_error
async def edit_inventory(inventory_id: str, inventory_update_data: InventoryUpdateModel = fastapi.Body(default=None),
                           user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    
    inventory_db.put_inventory(inventory_id=inventory_id, inventory_update_data=inventory_update_data)
    return {"info": "inventory successfully updated"}


@router.delete("/cinematic/inventory/{inventory_id}", tags=["inventory"], status_code=204)
@handle_db_error
async def delete_inventory(inventory_id: str,
                            user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    
    inventory_db.delete_inventory(inventory_id=inventory_id)
    return {"info": "inventory successfully deleted"}
