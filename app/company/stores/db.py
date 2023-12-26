from fastapi import HTTPException
import mysql.connector
from typing import List, Optional
from app.db_connection import mysql_connection
from app.company.stores.model import StoreModel, StoreCreateModel, StoreUpdateModel

connection = mysql_connection()

def get_all_stores_for_company(company_id: int) -> List[StoreModel]:
    query = "SELECT id, company_id, name, location, created_at FROM stores WHERE company_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (company_id,))
    rows = cursor.fetchall()
    cursor.close()
    return [StoreModel(id=row[0], company_id=row[1], name=row[2], location=row[3], created_at=row[4]) for row in rows]

def get_store_by_id(store_id: int) -> Optional[StoreModel]:
    query = "SELECT id, company_id, name, location, created_at FROM stores WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (store_id,))
    row = cursor.fetchone()
    cursor.close()
    return StoreModel(id=row[0], company_id=row[1], name=row[2], location=row[3], created_at=row[4]) if row else None

def create_store(store_data: StoreCreateModel, company_id: int):
    try:
        connection = mysql_connection()
        cursor = connection.cursor()

        query = "INSERT INTO stores (company_id, name, location) VALUES (%s, %s, %s)"
        values = (company_id, store_data.name, store_data.location)
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        print(f"Database Error: {e}")
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    finally:
        cursor.close()
        if connection.is_connected():
            connection.close()



def update_store(store_id: int, store: StoreUpdateModel) -> bool:
    updates = []
    values = []
    if store.name is not None:
        updates.append("name = %s")
        values.append(store.name)
    if store.location is not None:
        updates.append("location = %s")
        values.append(store.location)
    if not updates:
        return False
    query = "UPDATE stores SET " + ", ".join(updates) + " WHERE id = %s"
    values.append(store_id)
    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0

def delete_store(store_id: int) -> bool:
    query = "DELETE FROM stores WHERE id = %s"
    values = (store_id,)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


