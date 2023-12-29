from fastapi import HTTPException
import mysql.connector
from typing import List, Optional
from app.db_connection import mysql_connection
from app.services.model import ServiceModel, ServicePostModel, ServiceUpdateModel

connection = mysql_connection()


def get_all_services_for_company(company_id: int) -> List[ServiceModel]:
    query = "SELECT id, name, company_id, description, price, created_at FROM services WHERE company_id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(company_id,))
    rows = cursor.fetchall()
    cursor.close()
    return [ServiceModel(id = row[0],name = row[1],company_id = row[2], description = row[3], price = row[4], created_at= row[5]) for row in rows]

def get_service_by_id(service_id: int) -> Optional[ServiceModel]:
    query = "SELECT id, name, company_id, description, price, created_at FROM services WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query,(service_id,))
    row = cursor.fetchone()
    cursor.close()
    return ServiceModel(id = row[0],name = row[1],company_id = row[2], description= row [3], price = row[4], created_at= row[5]) if row else None

def create_service(service_data: ServicePostModel, company_id: int):
    try:
        connection = mysql_connection()
        cursor = connection.cursor()

        query = "INSERT INTO services (company_id,name,description,price) VALUES (%s,%s,%s,%s)"
        values = (company_id,service_data.name,service_data.description,service_data.price)
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