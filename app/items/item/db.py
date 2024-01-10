from app.db_connection import mysql_connection
from app.items.item.model import ItemModel, ItemCreateModel, ItemUpdateModel
from typing import List, Optional

connection = mysql_connection()


def post_item(item: ItemCreateModel, company_id : int):
    query = "INSERT INTO items (company_id, name, description, price, tax_percentage) VALUES (%s, %s, %s, %s, %s)"
    values = (company_id, item.name, item.description, item.price, item.tax_percentage)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def put_item(item_id: int, item: ItemUpdateModel) -> bool:
    updates = []
    values = []
    if item.company_id is not None:
        updates.append("company_id = %s")
        values.append(item.company_id)
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
    query = "UPDATE items SET " + ", ".join(updates) + " WHERE item_id = %s"
    values.append(item_id)
    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def delete_item(item_id: int) -> bool:
    query = "DELETE FROM items WHERE item_id = %s"
    values = (item_id,)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def get_all_items(company_id: int) -> List[ItemModel]:
    query = "SELECT item_id, company_id, name, description, price, tax_percentage FROM items WHERE company_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (company_id,))
    rows = cursor.fetchall()
    cursor.close()
    items = []
    for row in rows:
        item = ItemModel(item_id=row[0], company_id=row[1], name=row[2], description=row[3], price=row[4], tax_percentage=row[5])
        items.append(item)
    return items


def get_item_by_id(item_id: int, company_id: int) -> Optional[ItemModel]:
    query = "SELECT item_id, company_id, name, description, price, tax_percentage FROM items WHERE company_id = %s AND item_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (company_id, item_id))
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = {
            "item_id": result[0],
            "company_id": result[1],
            "name": result[2],
            "description": result[3],
            "price": result[4],
            "tax_percentage": result[5]
        }
        return ItemModel(**result_dict)
    else:
        return None
