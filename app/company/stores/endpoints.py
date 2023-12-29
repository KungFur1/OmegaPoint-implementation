from fastapi import APIRouter, Depends, HTTPException, Body
import fastapi
from app.company.stores.model import StoreModel, StoreCreateModel, StoreUpdateModel
from app.company.stores.db import get_all_stores_for_company, get_store_by_id, create_store, update_store, delete_store
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
from app.JWT_auth.user_identification import UserIdentification
from app.db_error_handler import handle_db_error
import app.users.check as users_check
import app.company.stores.check as check
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.db_error_handler import handle_db_error



router = fastapi.APIRouter()

@router.get("/cinematic/stores", tags=["store"], status_code=200)
@handle_db_error
async def get_all_stores(user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    company_id = get_complete_user_information(user_identification.id).company_id
    stores = get_all_stores_for_company(company_id)
    return {"data": stores}

@router.get("/cinematic/stores/{store_id}", tags=["store"], status_code=200)
@handle_db_error
async def get_store_details(store_id: int, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    user_info = get_complete_user_information(user_identification.id)
    store = get_store_by_id(store_id)
    
    if not store or store.company_id != user_info.company_id:
        raise HTTPException(status_code=404, detail="Store not found or access denied")
    
    return {"data": store}

@router.post("/cinematic/stores", tags=["store"], status_code=201)
@handle_db_error
async def create_store_endpoint(store_data: StoreCreateModel = Body(...), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    user_info = get_complete_user_information(user_identification.id)

    users_check.is_owner_or_manager(user_info)

    try:
        store_id = create_store(store_data, user_info.company_id)
        return {"info": "Store successfully created", "store_id": store_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating store: {e}")

@router.put("/cinematic/stores/{store_id}", tags=["store"], status_code=200)
@handle_db_error
async def update_store_details(store_id: int, store_data: StoreUpdateModel = fastapi.Body(default=None), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    user_info = get_complete_user_information(user_identification.id)
    store = check.store_exists(store_id)

    users_check.is_owner_or_manager(user_info)
    if store.company_id != user_info.company_id:
        raise HTTPException(status_code=403, detail="Access denied")

    updated = update_store(store_id, store_data)
    if not updated:
        raise HTTPException(status_code=400, detail="No updates performed")
    return {"info": "Store successfully updated"}

@router.delete("/cinematic/stores/{store_id}", tags=["store"], status_code=204)
@handle_db_error
async def delete_store_endpoint(store_id: int, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    user_info = get_complete_user_information(user_identification.id)
    store = check.store_exists(store_id)

    users_check.is_owner_or_manager(user_info)
    if store.company_id != user_info.company_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot delete stores of other companies")

    deleted = delete_store(store_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Unable to delete store")
    return {"info": "Store successfully deleted"}


