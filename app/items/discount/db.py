from app.db_connection import mysql_connection
from app.items.discount.model import ItemDiscountModel, ItemDiscountCreateModel
from typing import List, Optional

connection = mysql_connection()

def post_item_discount(item_id: int, discount: ItemDiscountCreateModel):
    query = "INSERT INTO ItemDiscounts (item_id, discount_amount) VALUES (%s, %s)"
    values = (item_id, discount.discount_amount)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def put_item_discount(discount_id: int, discount: ItemDiscountCreateModel) -> bool:
    query = "UPDATE ItemDiscounts SET discount_amount = %s WHERE discount_id = %s"
    values = (discount.discount_amount, discount_id)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def delete_item_discount(discount_id: int) -> bool:
    query = "DELETE FROM ItemDiscounts WHERE discount_id = %s"
    values = (discount_id,)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def get_item_discounts(item_id: int) -> List[ItemDiscountModel]:
    query = "SELECT discount_id, item_id, discount_amount FROM ItemDiscounts WHERE item_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (item_id,))
    rows = cursor.fetchall()
    cursor.close()
    discounts = []
    for row in rows:
        discount = ItemDiscountModel(discount_id=row[0], item_id=row[1], discount_amount=row[2])
        discounts.append(discount)
    return discounts
