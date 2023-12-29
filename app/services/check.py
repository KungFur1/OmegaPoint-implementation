from fastapi import HTTPException
import app.services.db as services_db


def service_exist(service_id: int):
    service = services_db.get_service_by_id(service_id)
    if service is None:
        raise HTTPException(status_code=404, detail= "Service not found")
    return service
