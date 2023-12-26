from datetime import datetime
from app.JWT_auth.authorization import get_complete_user_information
from app.db_connection import mysql_connection
from app.orders.model import OrderModel, OrderPostModel
from typing import List, Optional

connection = mysql_connection()

def post_order(new_order: OrderPostModel):
    # Start a transaction
    connection.start_transaction()

    try:
        format_strings = ','.join(['%s'] * len(new_order.products))
        price_query = f"SELECT id, price FROM items WHERE id IN ({format_strings})"
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
        order_values = (new_order.user_id, new_order.company_id, total_price, new_order.created_at, new_order.status)
        cursor = connection.cursor(buffered=True)
        cursor.execute(order_query, order_values)
        
        order_id = cursor.lastrowid

        item_query = (
            "INSERT INTO order_item (order_id, item_id, quantity) "
            "VALUES (%s, %s, %s)"
        )
        for item_id, quantity in zip(new_order.products, new_order.quantities):
            cursor.execute(item_query, (order_id, item_id, quantity))

        connection.commit()
        cursor.close()
        return {"info": "Order and order items created", "order_id": order_id}

    except Exception as e:
        connection.rollback()
        cursor.close()
        return {"error": str(e)}


def get_orders(user_id: int) -> List[OrderModel]:
    company_id = get_complete_user_information(user_id).company_id
    if company_id is None:
        id = user_id
        query = "SELECT id, user_id, company_id, total_price, created_at, status FROM orders WHERE user_id = %s"
    else:
        id = company_id
        query = "SELECT id, user_id, company_id, total_price, created_at, status FROM orders WHERE company_id = %s"
    
    cursor = connection.cursor()
    cursor.execute(query, (id,))
    orders = cursor.fetchall()
    cursor.close()

    order_models = []
    for order in orders:
        order_id = order[0]
        # Query to get order items
        item_query = "SELECT item_id, quantity FROM order_item WHERE order_id = %s"
        cursor = connection.cursor()
        cursor.execute(item_query, (order_id,))
        order_items = cursor.fetchall()
        cursor.close()

        # Extract products and quantities
        products = [item[0] for item in order_items]
        quantities = [item[1] for item in order_items]

        # Construct OrderModel
        order_model = OrderModel(
            id=order_id,
            user_id=order[1],
            company_id=order[2],
            products=products,
            quantities=quantities,
            total_price=order[3],
            created_at=order[4],
            status=order[5]
        )
        order_models.append(order_model)

    if order_models:
        return order_models
    else:
        return {"company_id": company_id, "error": "No orders found"}
