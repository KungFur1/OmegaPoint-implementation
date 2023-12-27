from fastapi import HTTPException
import app.items.discount.db as discount_db
import app.company.db as company_db
from app.JWT_auth.user_identification import UserIdentification
from app.users.db import get_user_company_data
from app.users.check import is_admin, is_owner

def item_exists(company_id: str, item_id: str):
    if discount_db.get_item_by_id(company_id=company_id, item_id=item_id) is None:
        raise HTTPException(status_code=404, detail="Item not found")

def inventory_exists(company_id: str, inventory_id: str):
    if discount_db.get_inventory_by_id(company_id=company_id, inventory_id=inventory_id) is None:
        raise HTTPException(status_code=404, detail="Inventory not found")

def check_manager_permission(user_identification: UserIdentification, company_id: str):
    user_company_data = get_user_company_data(user_id=user_identification.id)
    
    if is_admin(user_id=user_identification.id):
        return  # Admin has full access
    
    if user_company_data.company_id != company_id:
        raise HTTPException(status_code=403, detail="Permission denied")
