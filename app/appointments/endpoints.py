from fastapi import APIRouter, Depends, HTTPException, Body
import fastapi
from app.appointments.model import AppointmentModel, AppointmentPostModel, AppointmentUpdateModel, AppointmentsList
from app.appointments.db import get_all_appointments_for_company, get_appointment_by_id, create_appointment, update_appointment, delete_appointment, appointment_exists, check_times
from app.services.model import ServiceAvailabilityModel,ServiceModel
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
from app.JWT_auth.user_identification import UserIdentification
from app.db_error_handler import handle_db_error
import app.users.check as users_check
import app.appointments.check as check
import app.appointments.db as db
from datetime import datetime

router = fastapi.APIRouter()

@router.get("/cinematic/appointments", tags=["appointments"], status_code = 200)
@handle_db_error
async def get_all_appointments(company_id: int):
    appointments = get_all_appointments_for_company(company_id)
    return {"data": appointments}

@router.get("/cinematic/appointments/{appointment_id}", tags=["appointments"], status_code=200)
@handle_db_error
async def get_appointment_details(appointment_id: int, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):

    appointment = get_appointment_by_id(appointment_id) 
    return {"data": appointment}

@router.post("/cinematic/appointments", tags= ["appointments"], status_code=201)
@handle_db_error
async def create_appointment_endpoint(appointment_data: AppointmentPostModel = Body(...),user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):


    requested_start_time = appointment_data.start_time
    requested_end_time = appointment_data.end_time
    requested_date = appointment_data.appointment_date
       

    quantity = appointment_exists(appointment_data.service_id) 
    calculate = check_times(appointment_data.service_id)

    i = 0
    while i < quantity:
        if(requested_date == calculate[i].appointment_date and calculate[i].start_time <= requested_start_time <= calculate[i].end_time or calculate[i].start_time <= requested_end_time <= calculate[i].end_time):
            raise HTTPException(
                status_code=400,
                detail="Time conflict"
            )
        else:
            i+=1
    
    db.create_appointment(appointment_data)

    return {"info": "Appointment successfully created"}

    
@router.put("/cinematic/appointments/{appointment_id}",tags=["appointments"], status_code=200)
@handle_db_error
async def update_appointment_details(appointment_id: int, appointment_data: AppointmentUpdateModel= fastapi.Body(default=None), user_identification: UserIdentification =fastapi.Depends(authorization_wrapper)):


    requested_start_time = appointment_data.start_time
    requested_end_time = appointment_data.end_time
    requested_date = appointment_data.appointment_date
       

    quantity = appointment_exists(appointment_data.service_id)
    calculate = check_times(appointment_data.service_id)
    

    i = 0
    while i < quantity:
        if(appointment_id == calculate[i].id):
            break
        if(requested_date == calculate[i].appointment_date and calculate[i].start_time <= requested_start_time <= calculate[i].end_time or calculate[i].start_time <= requested_end_time <= calculate[i].end_time):
            
            raise HTTPException(
                status_code=400,
                detail="Time conflict"
            )
        else:
            i+=1
    
    db.update_appointment(appointment_id,appointment_data)
    return {"info": "appointment successfully updated"}

@router.delete("/cinematic/appointments/{appointment_id}", tags = ["appointments"], status_code=200)
@handle_db_error
async def delete_appointment_endpoint(appointment_id: int, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):

    db.delete_appointment(appointment_id)
    return {"info": "appointment successfully deleted"}