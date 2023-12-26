from app.db_connection import mysql_connection
from app.orders.model import OrderPostModel
from typing import List, Optional

connection = mysql_connection()

def post_order(new_order : OrderPostModel, user_id : int):
    query = (
        "INSERT INTO orders (user_id, company_id, total_price, created_at, status)"
        "VALUES (%s, %s, %s, %s, %s)"
    )
    new_order_values = (user_id, new_order.company_id, new_order.total_price, new_order.created_at, new_order.status)
    cursor = connection.cursor()
    cursor.execute(query, new_order_values)
    connection.commit()
    cursor.close()
    return {"info" : "order created"}