from fastapi import HTTPException
import mysql.connector
from typing import List, Optional
from app.db_connection import mysql_connection
from app.appointments.model import AppointmentModel,AppointmentPostModel,AppointmentUpdateModel, AppointmentsList
from datetime import time

connection = mysql_connection()

def get_all_appointments_for_company(company_id: int) -> List[AppointmentModel]:
    query = "SELECT id, service_id, company_id, user_id, appointment_date, start_time,end_time, price, created_at FROM appointments WHERE company_id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(company_id,))
    rows = cursor.fetchall()
    cursor.close()
    return [AppointmentModel(id = row[0], service_id = row[1],company_id = row[2], user_id= row[3], appointment_date = row[4],start_time = row[5], end_time = row[6], price = row[7], created_at= row[8]) for row in rows]

def get_appointment_by_id(appointment_id: int) -> Optional[AppointmentModel]:
    query = "SELECT id, service_id, company_id, user_id, appointment_date, start_time, end_time, price, created_at FROM appointments WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(appointment_id,))
    row = cursor.fetchone()
    cursor.close()
    return AppointmentModel(id = row[0], service_id = row[1],company_id = row[2], user_id= row[3], appointment_date = row[4], start_time = row[5], end_time = row[6], price = row[7], created_at=row [8]) if row else None

def create_appointment(appointment_data: AppointmentPostModel):
    
        query = "INSERT INTO appointments (service_id,company_id,user_id,appointment_date,start_time,end_time,price) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        values = (appointment_data.service_id, appointment_data.company_id, appointment_data.user_id, appointment_data.appointment_date, appointment_data.start_time,appointment_data.end_time,appointment_data.price)
        cursor = connection.cursor()
        cursor.execute(query,values)
        connection.commit()
        cursor.close()

def appointment_exists(service_id: int) -> int:
    
    query = "SELECT COUNT(*) FROM appointments WHERE service_id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(service_id,))
    result = cursor.fetchone()
    
    return result[0]
    
def check_times(service_id:int) -> List[AppointmentsList]:
    
    query = "SELECT id,appointment_date, start_time, end_time FROM appointments WHERE service_id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(service_id,))
    rows = cursor.fetchall()
    cursor.close()
    return [AppointmentsList(id = row [0], appointment_date= row[1], start_time= row[2], end_time= row[3]) for row in rows]
    
     
def update_appointment(appointment_id: int, appointment: AppointmentUpdateModel) -> bool:
    updates = []
    values = []
    if appointment.service_id is not None:
        updates.append("service_id = %s")
        values.append(appointment.service_id)
    if appointment.user_id is not None:
        updates.append("user_id = %s")
        values.append(appointment.user_id)
    if appointment.appointment_date is not None:
        updates.append("appointment_date = %s")
        values.append(appointment.appointment_date)
    if appointment.start_time is not None:
        updates.append("start_time = %s")
        values.append(appointment.start_time)
    if appointment.end_time is not None:
        updates.append("end_time = %s")
        values.append(appointment.end_time)
    if appointment.price is not None:
        updates.append("price = %s")
        values.append(appointment.price)
    if not updates:
        return False
    
    query = "UPDATE appointments SET " + ", ".join(updates) + " WHERE id = %s"
    values.append(appointment_id)
    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def delete_appointment(appointment_id: int) -> bool:
    query = "DELETE FROM appointments WHERE id = %s"
    values = (appointment_id,)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0