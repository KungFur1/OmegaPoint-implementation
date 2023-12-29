from fastapi import HTTPException
import app.appointments.db as appointments_db


def appointment_exist(appointment_id: int):
    appointment = appointments_db.get_appointment_by_id(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail= "Appointment not found")
    return appointment