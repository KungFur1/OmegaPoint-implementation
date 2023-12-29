from fastapi import HTTPException
import mysql.connector
from typing import List, Optional
from app.db_connection import mysql_connection
from app.appointments.model import AppointmentModel,AppointmentPostModel,AppointmentUpdateModel

connection = mysql_connection()

def get_all_appointments_for_company(company_id: int) -> List[AppointmentModel]:
    query = "SELECT id, name, company_id, user_id, appointment_date, price, created_at FROM appointments WHERE company_id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(company_id,))
    rows = cursor.fetchall()
    cursor.close()
    return [AppointmentModel(id = row[0], name = row[1],company_id = row[2], user_id= row[3], appointment_date = row[4], price = row[5], created_at= row[6]) for row in rows]

def get_appointment_by_id(appointment_id: int) -> Optional[AppointmentModel]:
    query = "SELECT id, name, company_id, user_id, appointment_date, price, created_at FROM appointments WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(appointment_id,))
    row = cursor.fetchone()
    cursor.close()
    return AppointmentModel(id = row[0], name = row[1],company_id = row[2], user_id= row[3], appointment_date = row[4], price = row[5], created_at=row [6]) if row else None

def create_appointment(appointment_data: AppointmentPostModel, company_id: int):
    try:
        connection = mysql_connection()
        cursor = connection.cursor()

        query = "INSERT INTO appointments (company_id,name,user_id,appointment_date,price) VALUES (%s,%s,%s,%s, %s)"
        values = (company_id, appointment_data.name, appointment_data.user_id, appointment_data.appointment_date, appointment_data.price)
        cursor.execute(query,values)
        connection.commit()
    except Exception as e:
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail = f"Database Error: {str(e)}")
    finally:
        cursor.close()
        if connection.is_connected():
            connection.close()

def update_appointment(appointment_id: int, appointment: AppointmentUpdateModel) -> bool:
    updates = []
    values = []
    if appointment.name is not None:
        updates.append("name = %s")
        values.append(appointment.name)
    if appointment.user_id is not None:
        updates.append("user_id = %s")
        values.append(appointment.user_id)
    if appointment.appointment_date is not None:
        updates.append("appointment_date = %s")
        values.append(appointment.appointment_date)
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