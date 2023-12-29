from app.db_connection import mysql_connection
from typing import List, Optional
from app.users.loyalty.model import LoyaltyModel, LoyaltyCreateModel

connection = mysql_connection()


def get_loyalty_by_company_id(company_id : int) -> List[LoyaltyModel]:
    query = "SELECT * FROM loyalty WHERE company_id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (company_id,))
    result = cursor.fetchall()
    cursor.close()
    return [LoyaltyModel(**record) for record in result]


def get_loyalty_by_id(loyalty_id : int) -> Optional[LoyaltyModel]:
    query = "SELECT * FROM loyalty WHERE id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (loyalty_id,))
    result = cursor.fetchone()
    cursor.close()
    return LoyaltyModel(**result) if result else None


def post_loyalty(loyalty_data : LoyaltyCreateModel):
    query = """
    INSERT INTO loyalty (company_id, created_by_id, name, description, discount_percent) 
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        loyalty_data.company_id, 
        loyalty_data.created_by_id, 
        loyalty_data.name, 
        loyalty_data.description, 
        loyalty_data.discount_percent
    )
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def delete_loyalty_by_id(loyalty_id: int) -> bool:
    query = "DELETE FROM loyalty WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (loyalty_id,))
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    return affected_rows > 0
