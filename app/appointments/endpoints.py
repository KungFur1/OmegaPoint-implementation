from fastapi import APIRouter, Depends, HTTPException, Body
import fastapi
from app.appointments.model import AppointmentModel, AppointmentPostModel, AppointmentUpdateModel
from app.appointments.db import get_all_appointments_for_company, get_appointment_by_id, create_appointment, update_appointment, delete_appointment
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
from app.JWT_auth.user_identification import UserIdentification
from app.db_error_handler import handle_db_error
import app.users.check as users_check
import app.appointments.check as check

router = fastapi.APIRouter()

@router.get("/cinematic/appointments", tags=["appointments"], status_code = 200)
@handle_db_error
async def get_all_appointments(user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    company_id = get_complete_user_information(user_identification.id).company_id
    appointments = get_all_appointments_for_company(company_id)
    return {"data": appointments}

@router.get("/cinematic/appointments/{appointment_id}", tags=["appointments"], status_code=200)
@handle_db_error
async def get_appointment_details(appointment_id: int, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    user_info = get_complete_user_information(user_identification.id)
    appointment = get_appointment_by_id(appointment_id)

    if not appointment or appointment.company_id != user_info.company_id:
        raise HTTPException(status_code=404, detail="Appointment not found or access denied")
    
    return {"data": appointment}

@router.post("/cinematic/appointments", tags= ["appointments"], status_code=201)
@handle_db_error
async def create_appointment_endpoint(appointment_data: AppointmentPostModel = Body(...), user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    user_info = get_complete_user_information(user_identification.id)

    users_check.is_owner_or_manager(user_info)

    try:
        appointment_id = create_appointment(appointment_data, user_info.company_id)
        return {"info": "Appointment successfully created", "appointment_id": appointment_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error creating appointment: {e}")
    
@router.put("/cinematic/appointments/{appointment_id}",tags=["appointments"], status_code=200)
@handle_db_error
async def update_appointment_details(appointment_id: int, appointment_data: AppointmentUpdateModel= fastapi.Body(default=None), user_identification: UserIdentification =fastapi.Depends(authorization_wrapper)):
    user_info = get_complete_user_information(user_identification.id)
    appointment = check.appointment_exist(appointment_id)
    
    users_check.is_owner_or_manager(user_info)
    if appointment.company_id != user_info.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    updated= update_appointment(appointment_id, appointment_data)
    if not updated:
        raise HTTPException(status_code=400,detail= "No updates performed")
    return {"info": "appointment successfully updated"}

@router.delete("/cinematic/appointments/{appointment_id}", tags = ["appointments"], status_code=204)
@handle_db_error
async def delete_appointment_endpoint(appointment_id: int, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    user_info = get_complete_user_information(user_identification.id)
    appointment = check.appointment_exist(appointment_id)

    users_check.is_owner_or_manager(user_info)
    if appointment.company_id != user_info.company_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot delete appointments of other companies")
    
    deleted = delete_appointment(appointment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Unable to delete appointment")
    return {"info": "appointment successfully deleted"}