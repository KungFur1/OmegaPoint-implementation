from app.db_connection import mysql_connection
from app.items.inventory.model import InventoryUpdateModel, InventoryCreateModel, InventoryModel
from typing import List, Optional

connection = mysql_connection()

def post_inventory(inventory: InventoryCreateModel):
    query = "INSERT INTO Inventory (item_id, store_id, quantity) VALUES (%s, %s, %s)"
    values = (inventory.item_id, inventory.store_id, inventory.quantity)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def put_inventory(inventory_id: int, inventory: InventoryUpdateModel) -> bool:
    query = "UPDATE Inventory SET quantity = %s WHERE inventory_id = %s"
    values = (inventory.quantity, inventory_id)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def delete_inventory(inventory_id: int) -> bool:
    query = "DELETE FROM Inventory WHERE inventory_id = %s"
    values = (inventory_id,)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0

def get_inventory_items(item_id: int) -> List[InventoryModel]:
    query = "SELECT inventory_id, item_id, store_id, quantity FROM Inventory WHERE item_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (item_id,))
    rows = cursor.fetchall()
    cursor.close()
    inventory_items = []
    for row in rows:
        inventory_item = InventoryModel(inventory_id=row[0], item_id=row[1], store_id=row[2], quantity=row[3])
        inventory_items.append(inventory_item)
    return inventory_items

def get_inventory_by_id(inventory_id: str) -> Optional[InventoryModel]:
    query = "SELECT inventory_id, item_id, store_id, quantity FROM Inventory WHERE inventory_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (inventory_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = {
            "inventory_id": result[0],
            "item_id": result[1],
            "store_id": result[2],
            "quantity": result[3],
        }
        return InventoryModel(**result_dict)
    else:
        return None
    
def get_all_inventory() -> List[InventoryModel]:
    query = "SELECT inventory_id, item_id, store_id, quantity FROM Inventory"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    inventories = []
    for row in rows:
        inventory = InventoryModel(inventory_id=row[0], item_id=row[1], store_id=row[2], quantity=row[3])
        inventories.append(inventory)
    return inventories