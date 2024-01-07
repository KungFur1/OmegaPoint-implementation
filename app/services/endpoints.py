from fastapi import APIRouter, Depends, HTTPException, Body
import fastapi
from app.services.model import ServiceModel,ServicePostModel,ServiceUpdateModel, ServiceAvailabilityModel
from app.services.db import get_all_services_for_company,get_service_by_id, create_service,update_service,delete_service, get_service_availability, create_service_availability
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
from app.JWT_auth.user_identification import UserIdentification
from app.db_error_handler import handle_db_error
import app.users.check as users_check
import app.services.check as check
import app.services.db as db


router = fastapi.APIRouter()

@router.get("/cinematic/services", tags=["services"], status_code = 200)
@handle_db_error
async def get_all_services(user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    company_id = get_complete_user_information(user_identification.id).company_id
    services = get_all_services_for_company(company_id)
    return {"data": services}

@router.get("/cinematic/services/{service_id}", tags=["services"], status_code=200)
@handle_db_error
async def get_service_details(service_id: int):
 
    service = get_service_by_id(service_id)
    return {"data": service}

@router.post("/cinematic/services", tags= ["services"], status_code=201)
@handle_db_error
async def create_service_endpoint(service_data: ServicePostModel = Body(...), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
        
        db.create_service(service_data)
        return {"info": "Service successfully created"}

    
@router.put("/cinematic/services/{service_id}",tags=["services"], status_code=200)
@handle_db_error
async def update_service_details(service_id: int, service_data: ServiceUpdateModel= fastapi.Body(default=None), user_identification: UserIdentification =fastapi.Depends(authorization_wrapper)):

    db.update_service(service_id,service_data)
    return {"info": "Service successfully updated"}

@router.delete("/cinematic/services/{service_id}", tags = ["services"], status_code=200)
@handle_db_error
async def delete_service_endpoint(service_id: int, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):

    db.delete_service(service_id)
    return {"info": "Service successfully deleted"}


@router.get("/cinematic/services/serviceAvailability/{service_id}", tags=["services"], status_code=200)
@handle_db_error
async def get_service_availability(service_id: int):
 
  return {"data" : db.get_service_availability(service_id=service_id)}

@router.post("/cinematic/services/serviceAvailability/{service_id}", tags= ["services"], status_code=201)
@handle_db_error
async def create_service_Availability_time(service_availability_data: ServiceAvailabilityModel = fastapi.Body(default=None), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    db.create_service_availability(service_availability_data)
    return {"info": "Working time successfully created"}

