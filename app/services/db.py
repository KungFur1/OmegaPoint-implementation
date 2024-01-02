from fastapi import HTTPException
import mysql.connector
from typing import List, Optional
from app.db_connection import mysql_connection
from app.services.model import ServiceModel, ServicePostModel, ServiceUpdateModel, ServiceAvailabilityModel

connection = mysql_connection()


def get_all_services_for_company(company_id: int) -> List[ServiceModel]:
    query = "SELECT id, name, company_id, description, price,time, created_at FROM services"
    cursor = connection.cursor()
    cursor.execute(query,)
    rows = cursor.fetchall()
    cursor.close()
    return [ServiceModel(id = row[0],name = row[1],company_id = row[2], description = row[3], price = row[4], time = row[5], created_at= row[6]) for row in rows]

def get_service_by_id(service_id: int) -> Optional[ServiceModel]:
    query = "SELECT id, name, company_id, description, price, time, created_at FROM services WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(service_id,))
    row = cursor.fetchone()
    cursor.close()
    return ServiceModel(id = row[0],name = row[1],company_id = row[2], description= row [3], price = row[4], time = row [5], created_at= row[6]) if row else None

def create_service(service_data: ServicePostModel, company_id: int):
    try:
        connection = mysql_connection()
        cursor = connection.cursor()

        query = "INSERT INTO services (company_id,name,description,price,time) VALUES (%s,%s,%s,%s,%s)"
        values = (company_id,service_data.name,service_data.description,service_data.price, service_data.time)
        cursor.execute(query,values)
        connection.commit()
    except Exception as e:
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail = f"Database Error: {str(e)}")
    finally:
        cursor.close()
        if connection.is_connected():
            connection.close()

def update_service(service_id: int, service: ServiceUpdateModel) -> bool:
    updates = []
    values = []
    if service.name is not None:
        updates.append("name = %s")
        values.append(service.name)
    if service.description is not None:
        updates.append("description = %s")
        values.append(service.description)
    if service.price is not None:
        updates.append("price = %s")
        values.append(service.price)
    if service.time is not None:
        updates.append("time = %s")
        values.append(service.time)
    if not updates:
        return False
    
    query = "UPDATE services SET " + ", ".join(updates) + " WHERE id = %s"
    values.append(service_id)
    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0

def delete_service(service_id: int) -> bool:
    query = "DELETE FROM services WHERE id = %s"
    values = (service_id,)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0
     
def get_service_availability(service_id: int) -> Optional[ServiceAvailabilityModel]:
    query = "SELECT id, service_id,start_date,end_date FROM service_availability WHERE service_id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(service_id,))
    row = cursor.fetchone()
    cursor.close()
    return ServiceAvailabilityModel(id = row[0], service_id = row[1],start_date = row[2], end_date= row [3]) if row else None


    