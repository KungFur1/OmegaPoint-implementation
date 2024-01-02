from fastapi import APIRouter, Depends, HTTPException, Body
import fastapi
from app.appointments.model import AppointmentModel, AppointmentPostModel, AppointmentUpdateModel
from app.appointments.db import get_all_appointments_for_company, get_appointment_by_id, create_appointment, update_appointment, delete_appointment
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
from app.JWT_auth.user_identification import UserIdentification
from app.db_error_handler import handle_db_error
import app.users.check as users_check
import app.appointments.check as check
import app.appointments.db as db

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
async def create_appointment_endpoint(appointment_data: AppointmentPostModel = Body(...), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):

    db.create_appointment(appointment_data)

    return {"info": "Appointment successfully created"}

    
@router.put("/cinematic/appointments/{appointment_id}",tags=["appointments"], status_code=200)
@handle_db_error
async def update_appointment_details(appointment_id: int, appointment_data: AppointmentUpdateModel= fastapi.Body(default=None), user_identification: UserIdentification =fastapi.Depends(authorization_wrapper)):

    db.update_appointment(appointment_id,appointment_data)
    return {"info": "appointment successfully updated"}

@router.delete("/cinematic/appointments/{appointment_id}", tags = ["appointments"], status_code=204)
@handle_db_error
async def delete_appointment_endpoint(appointment_id: int, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):

    db.delete_appointment(appointment_id)
    return {"info": "appointment successfully deleted"}