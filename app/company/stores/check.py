from fastapi import HTTPException
import app.company.stores.db as store_db

def store_exists(store_id: int):
    store = store_db.get_store_by_id(store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return store  
