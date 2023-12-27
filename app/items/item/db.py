from app.db_connection import mysql_connection
from app.items.item.model import ItemModel, ItemCreateModel, ItemUpdateModel
from typing import List, Optional

connection = mysql_connection()


def post_item(item: ItemCreateModel):
    query = "INSERT INTO Items (name, description, price, tax_percentage) VALUES (%s, %s, %s, %s)"
    values = (item.name, item.description, item.price, item.tax_percentage)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def put_item(item_id: int, item: ItemUpdateModel) -> bool:
    updates = []
    values = []
    if item.name is not None:
        updates.append("name = %s")
        values.append(item.name)
    if item.description is not None:
        updates.append("description = %s")
        values.append(item.description)
    if item.price is not None:
        updates.append("price = %s")
        values.append(item.price)
    if item.tax_percentage is not None:
        updates.append("tax_percentage = %s")
        values.append(item.tax_percentage)
    if not updates:
        return False
    query = "UPDATE Items SET " + ", ".join(updates) + " WHERE item_id = %s"
    values.append(item_id)
    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def delete_item(item_id: int) -> bool:
    query = "DELETE FROM Items WHERE item_id = %s"
    values = (item_id,)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def get_all_items() -> List[ItemModel]:
    query = "SELECT item_id, name, description, price, tax_percentage FROM Items"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    items = []
    for row in rows:
        item = ItemModel(item_id=row[0], name=row[1], description=row[2], price=row[3], tax_percentage=row[4])
        items.append(item)
    return items


def get_item_by_id(item_id: int) -> Optional[ItemModel]:
    query = "SELECT item_id, name, description, price, tax_percentage FROM Items WHERE item_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (item_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = {
            "item_id": result[0],
            "name": result[1],
            "description": result[2],
            "price": result[3],
            "tax_percentage": result[4],
        }
        return ItemModel(**result_dict)
    else:
        return None
