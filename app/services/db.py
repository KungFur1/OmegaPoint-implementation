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

def create_service(service_data: ServicePostModel):

        query = "INSERT INTO services (name,company_id,description,price,time) VALUES (%s,%s,%s,%s,%s)"
        values = (service_data.name,service_data.company_id,service_data.description,service_data.price, service_data.time)
        cursor = connection.cursor()
        cursor.execute(query,values)
        connection.commit()
        cursor.close()


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
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = {
            "id" : result[0],
            "service_id" : result[1],
            "start_date" : result[2],
            "end_date" : result[3]
        }
        return ServiceAvailabilityModel(**result_dict)
    else:
        return None


def create_service_availability(service_data: ServiceAvailabilityModel):
    
        query = "INSERT INTO service_availability (service_id,start_date,end_date) VALUES (%s,%s,%s)"
        values = (service_data.service_id, service_data.start_date,service_data.end_date)
        cursor = connection.cursor()
        cursor.execute(query,values)
        connection.commit()
        cursor.close()

    