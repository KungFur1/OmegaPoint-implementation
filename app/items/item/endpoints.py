import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.items.item.model import ItemCreateModel, ItemUpdateModel
import app.items.item.db as item_db
import app.users.db as users_db
from app.db_error_handler import handle_db_error
import app.users.check as users_check
from app.company.stores.db import get_all_stores_for_company
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information

router = fastapi.APIRouter()


@router.get("/cinematic/items", tags=["items"], status_code=200)
@handle_db_error
async def get_all_items(user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)): 
    
    company_id = get_complete_user_information(user_identification.id).company_id
    
    items = item_db.get_all_items(company_id)
       
    return {"data": items}


@router.get("/cinematic/items/{item_id}", tags=["items"], status_code=200)
@handle_db_error
async def get_item_by_id(item_id: str, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    
    company_id = get_complete_user_information(user_identification.id).company_id
    
    item = item_db.get_item_by_id(item_id, company_id)
    
    return {"data": item}


@router.post("/cinematic/items", tags=["items"], status_code=201)
@handle_db_error
async def create_item(item_create_data: ItemCreateModel = fastapi.Body(default=None), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    
    company_id = get_complete_user_information(user_identification.id).company_id
    
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    users_check.is_employee_or_higher(user_company_data=auth_user_cd)
    
    item_db.post_item(item_create_data, company_id)
    
    return {"info": "item successfully inserted"}


@router.put("/cinematic/items/{item_id}", tags=["items"], status_code=200)
@handle_db_error
async def edit_item(item_id: str, item_update_data: ItemUpdateModel = fastapi.Body(default=None), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    users_check.is_employee_or_higher(user_company_data=auth_user_cd)
    
    item_db.put_item(item_id, item_update_data)
    
    return {"info": "item successfully updated"}


@router.delete("/cinematic/items/{item_id}", tags=["items"], status_code=204)
@handle_db_error
async def delete_item(item_id: str, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
        
    auth_user_cd = users_db.get_user_company_data(user_id=user_identification.id)
    users_check.is_employee_or_higher(user_company_data=auth_user_cd)
    
    item_db.delete_item(item_id)
    return {"info": "item successfully deleted"}


