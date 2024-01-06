from datetime import datetime
from fastapi import HTTPException
from app.JWT_auth.authorization import get_complete_user_information
from app.JWT_auth.user_identification import UserIdentification
from app.db_connection import mysql_connection
from app.orders.model import AddOrderItemModel, OrderModel, OrderPostModel, OrderStatuses, OrderUpdateModel
from typing import List, Optional

from app.users.model import CompanyPositions
from app.users.roles.access_handler import get_user_access

def post_order(new_order: OrderPostModel, user_id):
    connection = mysql_connection()
    # Start a transaction
    connection.start_transaction()
    cursor = connection.cursor(buffered=True)
    try:
        format_strings = ','.join(['%s'] * len(new_order.products))
        price_query = f"SELECT item_id, price FROM items WHERE item_id IN ({format_strings})"
        price_cursor = connection.cursor(buffered=True)
        # Execute the query with the list of product IDs
        price_cursor.execute(price_query, tuple(new_order.products))

        # Fetch the prices
        prices = {id: price for id, price in price_cursor.fetchall()}
        price_cursor.close()

        total_price = sum(prices[item_id] * quantity for item_id, quantity in zip(new_order.products, new_order.quantities))

        order_query = (
            "INSERT INTO orders (user_id, company_id, total_price, created_at, status) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        order_values = (user_id, new_order.company_id, total_price, new_order.created_at, new_order.status)
        cursor.execute(order_query, order_values)
        
        order_id = cursor.lastrowid

        item_query = (
            "INSERT INTO order_item (order_id, item_id, quantity) "
            "VALUES (%s, %s, %s)"
        )
        for item_id, quantity in zip(new_order.products, new_order.quantities):
            cursor.execute(item_query, (order_id, item_id, quantity))

        connection.commit()
        return {"info": "Order and order items created", "order_id": order_id}

    except Exception as e:
        connection.rollback()
        return {"error": str(e)}
    finally:
        connection.disconnect()
        connection.close()
        cursor.close()


def get_orders(user_id: int) -> List[OrderModel]:
    connection = mysql_connection()

    company_id = get_complete_user_information(user_id).company_id
    if company_id is None:
        id = ("user_id", user_id)
        query = "SELECT id, user_id, assignee_id, company_id, total_price, created_at, updated_at, status FROM orders WHERE user_id = %s"
    else:
        id = ("company_id", company_id)
        query = "SELECT id, user_id, assignee_id, company_id, total_price, created_at, updated_at, status FROM orders WHERE company_id = %s"
    
    cursor_orders = connection.cursor()
    cursor_order_item = connection.cursor()
    try:
        cursor_orders.execute(query, (id[1],))
        orders = cursor_orders.fetchall()

        order_models = []
        for order in orders:
            order_id = order[0]
            # Query to get order items
            item_query = "SELECT item_id, quantity FROM order_item WHERE order_id = %s"
            cursor_order_item.execute(item_query, (order_id,))
            order_items = cursor_order_item.fetchall()

            # Extract products and quantities
            products = [item[0] for item in order_items]
            quantities = [item[1] for item in order_items]

            # Construct OrderModel
            order_model = OrderModel(
                id=order_id,
                user_id=order[1],
                assignee_id=order[2],
                company_id=order[3],
                products=products,
                quantities=quantities,
                total_price=order[4],
                created_at=order[5],
                updated_at=order[6],
                status=order[7]
            )
            order_models.append(order_model)

        if order_models:
            return order_models
        else:
            return {id[0]: id[1], "error": "No orders found"}
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor_orders.close()
        cursor_order_item.close()
        connection.disconnect()
        connection.close()


def get_order(order_id: int, user_id: int) -> OrderModel | None:
    connection = mysql_connection()

    company_id = get_complete_user_information(user_id).company_id
    if company_id is None:
        id = ("user_id", user_id)
        query = "SELECT id, user_id, assignee_id, company_id, total_price, created_at, updated_at, status FROM orders WHERE user_id = %s AND id = %s"
    else:
        id = ("company_id", company_id)
        query = "SELECT id, user_id, assignee_id, company_id, total_price, created_at, updated_at, status FROM orders WHERE company_id = %s AND id = %s"
    
    cursor_orders = connection.cursor()
    cursor_order_item = connection.cursor()
    try:
        cursor_orders.execute(query, (id[1], order_id))
        order = cursor_orders.fetchone()

        if order:
            # Query to get order items
            item_query = "SELECT item_id, quantity FROM order_item WHERE order_id = %s"
            cursor_order_item.execute(item_query, (order_id,))
            order_items = cursor_order_item.fetchall()

            # Extract products and quantities
            products = [item[0] for item in order_items]
            quantities = [item[1] for item in order_items]

            # Construct OrderModel
            order_model = OrderModel(
                id=order[0],
                user_id=order[1],
                assignee_id=order[2],
                company_id=order[3],
                products=products,
                quantities=quantities,
                total_price=order[4],
                created_at=order[5],
                updated_at=order[6],
                status=order[7]
            )
            return order_model
        else:
            return {id[0]: id[1], "error": "No orders found"}
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor_orders.close()
        cursor_order_item.close()
        connection.disconnect()
        connection.close()

# ! Employee only
def update_order(order_id: int, new_order: OrderUpdateModel, user_id: int):
    access = get_user_access(user_id)
    if access.payments_manage is False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    connection = mysql_connection()
    connection.start_transaction()
    price_cursor = connection.cursor(buffered=True)
    cursor = connection.cursor(buffered=True)

    is_order_in_company(order_id, user_id)

    format_strings = ','.join(['%s'] * len(new_order.products))
    price_query = f"SELECT item_id, price FROM items WHERE item_id IN ({format_strings})"
    # Execute the query with the list of product IDs
    price_cursor.execute(price_query, tuple(new_order.products))

    # Fetch the prices
    prices = {id: price for id, price in price_cursor.fetchall()}

    total_price = sum(prices[item_id] * quantity for item_id, quantity in zip(new_order.products, new_order.quantities))

    order_query = (
        "UPDATE orders SET company_id = %s, assignee_id = %s, total_price = %s, updated_at = %s, status = %s "
        "WHERE id = %s"
    )
    order_values = (new_order.company_id, new_order.assignee_id, total_price, new_order.updated_at, new_order.status, order_id)
    cursor.execute(order_query, order_values)
    
    item_query = (
        "DELETE FROM order_item WHERE order_id = %s"
    )
    cursor.execute(item_query, (order_id,))

    item_query = (
        "INSERT INTO order_item (order_id, item_id, quantity) "
        "VALUES (%s, %s, %s)"
    )
    for item_id, quantity in zip(new_order.products, new_order.quantities):
        cursor.execute(item_query, (order_id, item_id, quantity))

    connection.commit()
    cursor.close()
    price_cursor.close()
    connection.disconnect()
    connection.close()

    return {"info": "Order and order items updated", "order_id": order_id}


def delete_order(order_id: int, user_id: int):
    access = get_user_access(user_id)
    if access.payments_manage is False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    connection = mysql_connection()
    connection.start_transaction()
    cursor = connection.cursor(buffered=True)

    is_order_in_company(order_id, user_id)

    item_query = (
        "DELETE FROM order_item WHERE order_id = %s"
    )
    cursor.execute(item_query, (order_id,))

    order_query = (
        "DELETE FROM orders WHERE id = %s"
    )
    cursor.execute(order_query, (order_id,))

    connection.commit()
    cursor.close()
    connection.disconnect()
    connection.close()

    return {"info": "Order and order items deleted", "order_id": order_id}


def update_order_status(order_id: int, new_status: OrderStatuses, user_id: int):
    access = get_user_access(user_id)
    if access.payments_manage is False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    connection = mysql_connection()
    connection.start_transaction()
    cursor = connection.cursor(buffered=True)

    updated_at = datetime.now()
    is_order_in_company(order_id, user_id)

    order_query = (
        "UPDATE orders SET status = %s, updated_at = %s "
        "WHERE id = %s"
    )
    order_values = (new_status.value, updated_at, order_id)
    cursor.execute(order_query, order_values)

    connection.commit()
    cursor.close()
    connection.disconnect()
    connection.close()

    return {"info": "Order status updated", "order_id": order_id}


def assign_order(order_id: int, assignee_id: int, user_id: int):
    access = get_user_access(user_id)
    assignee_company_id = get_complete_user_information(assignee_id).company_id
    user_company_id = get_complete_user_information(user_id).company_id
    if assignee_company_id != user_company_id or access.payments_manage is False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    connection = mysql_connection()
    connection.start_transaction()
    cursor = connection.cursor(buffered=True)

    is_order_in_company(order_id, user_id)

    order_query = (
        "UPDATE orders SET assignee_id = %s, updated_at = %s "
        "WHERE id = %s"
    )
    updated_at = datetime.now()
    order_values = (assignee_id, updated_at, order_id)
    cursor.execute(order_query, order_values)

    connection.commit()
    cursor.close()
    connection.disconnect()
    connection.close()
    
    return {"info": "Order assigned", "order_id": order_id}        


def add_order_item(order_id, order_item: AddOrderItemModel, user_id: int):
    access = get_user_access(user_id)
    if access.payments_manage is False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    connection = mysql_connection()
    connection.start_transaction()
    cursor = connection.cursor(buffered=True)

    is_order_in_company(order_id, user_id)

    order_query = "SELECT id FROM orders WHERE id = %s"
    cursor.execute(order_query, (order_id,))
    if cursor.rowcount == 0:
        raise Exception(f"{order_id} order_id not found")

    item_query = "SELECT item_id FROM items WHERE item_id = %s"
    cursor.execute(item_query, (order_item.item_id,))
    if cursor.rowcount == 0:
        raise Exception(f"{order_item.item_id} item_id not found")
    
    # Calculate the price of the items
    price_query = "SELECT price FROM items WHERE item_id = %s"
    cursor.execute(price_query, (order_item.item_id,))
    price = cursor.fetchone()[0]
    order_item_price = price * order_item.quantity

    # Update the total price of the order
    order_query = (
        "UPDATE orders SET total_price = total_price + %s "
        "WHERE id = %s"
    )
    order_values = (order_item_price, order_id)
    cursor.execute(order_query, order_values)

    item_query = (
        "INSERT INTO order_item (order_id, item_id, quantity) "
        "VALUES (%s, %s, %s)"
    )
    cursor.execute(item_query, (order_id, order_item.item_id, order_item.quantity))
    
    connection.commit()
    cursor.close()
    connection.disconnect()
    connection.close()
    
    return {"info": "Order item added", "order_id": order_id, "item_id": order_item.item_id, "order_item_id": cursor.lastrowid}


def delete_order_item(order_id, order_item_id, user_id):
    access = get_user_access(user_id)
    if access.payments_manage is False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    connection = mysql_connection()
    connection.start_transaction()
    cursor = connection.cursor(buffered=True)

    is_order_item_in_company(order_item_id, user_id)

    order_query = "SELECT id FROM orders WHERE id = %s"
    cursor.execute(order_query, (order_id,))

    #Get item_id from order_item table
    item_query = "SELECT item_id FROM order_item WHERE id = %s"
    cursor.execute(item_query, (order_item_id,))
    item_id = cursor.fetchone()[0]

    item_query = "SELECT item_id FROM items WHERE item_id = %s"
    cursor.execute(item_query, (item_id,))
    if cursor.rowcount == 0:
        raise Exception(f"{order_item_id} item_id not found")
    
    # Calculate the price of the items
    price_query = "SELECT price FROM items WHERE item_id = %s"
    cursor.execute(price_query, (item_id,))
    price = cursor.fetchone()
    if price is None:
        raise HTTPException(status_code=404, detail=f"{order_item_id} order_item_id not found")

    # Calculate the quantity of the items
    quantity_query = "SELECT quantity FROM order_item WHERE order_id = %s AND item_id = %s"
    cursor.execute(quantity_query, (order_id, item_id))
    quantity = cursor.fetchone()[0]
    order_item_price = price[0] * quantity

    # Update the total price of the order
    order_query = (
        "UPDATE orders SET total_price = total_price - %s "
        "WHERE id = %s"
    )
    order_values = (order_item_price, order_id)
    cursor.execute(order_query, order_values)

    item_query = (
        "DELETE FROM order_item WHERE order_id = %s AND id = %s"
    )
    cursor.execute(item_query, (order_id, order_item_id))
    
    connection.commit()
    cursor.close()
    connection.disconnect()
    connection.close()

    return {"info": "Order item deleted", "order_id": order_id, "item_id": order_item_id}


def get_order_items(unassigned: bool, user_id: int):
    access = get_user_access(user_id)
    if access.payments_read is False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    connection = mysql_connection()
    connection.start_transaction()
    
    cursor = connection.cursor(buffered=True)

    company_id = get_complete_user_information(user_id).company_id
    order_query = "SELECT id FROM orders WHERE company_id = %s"
    cursor.execute(order_query, (company_id,))

    order_ids = [order[0] for order in cursor.fetchall()]

    if not order_ids:
        return {"error": "No orders found"}

    format_strings = ','.join(['%s'] * len(order_ids))

    if unassigned:
        item_query = f"SELECT order_id, item_id, assignee_id, quantity, status FROM order_item WHERE order_id IN ({format_strings}) AND assignee_id IS NULL"
    else:
        item_query = f"SELECT order_id, item_id, assignee_id, quantity, status FROM order_item WHERE order_id IN ({format_strings}) AND assignee_id IS NOT NULL"

    cursor.execute(item_query, tuple(order_ids))

    order_items = cursor.fetchall()

    order_items_dict = {}
    for order_item in order_items:
        order_id = order_item[0]
        item_id = order_item[1]
        assignee_id = order_item[2]
        quantity = order_item[3]
        status = order_item[4]

        if order_id not in order_items_dict:
            order_items_dict[order_id] = []

        order_items_dict[order_id].append({"item_id": item_id, "assignee_id": assignee_id, "quantity": quantity, "status": status})

    cursor.close()
    connection.disconnect()
    connection.close()
    
    return order_items_dict


def get_order_item(order_item_id: int, user_id: int):
    access = get_user_access(user_id)
    if access.payments_read is False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    connection = mysql_connection()
    connection.start_transaction()
    cursor = connection.cursor(buffered=True)

    company_id = get_complete_user_information(user_id).company_id

    is_order_item_in_company(order_item_id, user_id)

    order_query = "SELECT id FROM orders WHERE company_id = %s"
    cursor.execute(order_query, (company_id,))

    order_ids = [order[0] for order in cursor.fetchall()]

    format_strings = ','.join(['%s'] * len(order_ids))

    item_query = f"SELECT order_id, item_id, assignee_id, quantity, status FROM order_item WHERE order_id IN ({format_strings}) AND id = %s"

    cursor.execute(item_query, tuple(order_ids) + (order_item_id,))

    order_item = cursor.fetchone()

    order_id = order_item[0]
    item_id = order_item[1]
    assignee_id = order_item[2]
    quantity = order_item[3]
    status = order_item[4]

    cursor.close()
    connection.disconnect()
    connection.close()
    
    return {"order_id": order_id, "item_id": item_id, "assignee_id": assignee_id, "quantity": quantity, "status": status}


def update_order_item_status(order_item_id: int, new_status: OrderStatuses, user_id: int):
    access = get_user_access(user_id)
    if access.payments_manage is False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    connection = mysql_connection()
    connection.start_transaction()
    cursor = connection.cursor(buffered=True)

    is_order_item_in_company(order_item_id, user_id)

    order_query = (
        "UPDATE order_item SET status = %s "
        "WHERE id = %s"
    )
    order_values = (new_status.value, order_item_id)
    cursor.execute(order_query, order_values)

    connection.commit()
    cursor.close()
    connection.disconnect()
    connection.close()
    
    return {"info": "Order item status updated", "order_item_id": order_item_id}


def assign_order_item(order_item_id: int, assignee_id: int, user_id: int):
    access = get_user_access(user_id)
    assignee_company_id = get_complete_user_information(assignee_id).company_id
    user_company_id = get_complete_user_information(user_id).company_id
    if assignee_company_id != user_company_id or access.payments_manage is False:
        raise HTTPException(status_code=401, detail="Unauthorized")

    connection = mysql_connection()
    connection.start_transaction()
    cursor = connection.cursor(buffered=True)

    is_order_item_in_company(order_item_id, user_id)

    order_query = (
        "UPDATE order_item SET assignee_id = %s "
        "WHERE id = %s"
    )
    order_values = (assignee_id, order_item_id)
    cursor.execute(order_query, order_values)

    connection.commit()
    cursor.close()
    connection.disconnect()
    connection.close()
    
    return {"info": "Order item assigned", "order_item_id": order_item_id}


def is_order_in_company(order_id: int, user_id: int):
    connection = mysql_connection()
    company_id = get_complete_user_information(user_id).company_id

    cursor = connection.cursor(buffered=True)
    order_query = "SELECT id FROM orders WHERE id = %s AND company_id = %s"
    cursor.execute(order_query, (order_id, company_id))

    connection.close()
    cursor.close()
    
    return True


def is_order_item_in_company(order_item_id: int, user_id: int):
    connection = mysql_connection()
    cursor = connection.cursor(buffered=True)
    company_id = get_complete_user_information(user_id).company_id

    cursor.execute("""
        SELECT oi.id
        FROM order_item oi
        JOIN orders o ON oi.order_id = o.id
        WHERE o.company_id = %s AND oi.id = %s
        LIMIT 1
    """, (company_id, order_item_id))

    result = cursor.fetchone()

    connection.close()
    cursor.close()

    if result is None:
        raise HTTPException(status_code=404, detail=f"{order_item_id} order_item_id not found")

    return True

