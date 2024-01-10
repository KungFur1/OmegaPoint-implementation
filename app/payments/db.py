import datetime
from app.JWT_auth.authorization import get_complete_user_information
from app.db_connection import mysql_connection
from app.orders.db import is_order_in_company
from app.orders.model import OrderModel, OrderStatuses
from .model import VAT_RATE, PaymentMethod, PaymentModel, PaymentStatuses
from datetime import datetime
import time
import mysql.connector
from typing import Optional
from .model import PaymentModel


def create_payment(payment_data: PaymentModel, user_id: int):
    connection = mysql_connection()
    try:
        connection.start_transaction()

        if not is_order_in_company(payment_data.order_id, user_id):
            raise ValueError("Order does not exist or does not belong to the user's company")

        order = get_order_for_payment(payment_data.order_id, user_id)
        if not order:
            raise ValueError("Order not found")

        total_due, tax, discount = calculate_total_due(order, payment_data)

        if payment_data.payment_method == PaymentMethod.CARD.value:
            amount_to_charge = total_due + (payment_data.tip if payment_data.tip > 0 else 0)
            payment_data.amount = round(amount_to_charge, 2)  # Update the amount for card payments

        payment_query = """
            INSERT INTO payments (order_id, user_id, amount, tip, payment_method, payment_status, discount_percentage, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        payment_values = (
            payment_data.order_id, user_id, payment_data.amount,
            payment_data.tip, payment_data.payment_method, PaymentStatuses.PENDING.value,
            payment_data.discount_percentage, datetime.now()
        )

        cursor = connection.cursor(buffered=True)
        cursor.execute(payment_query, payment_values)
        payment_id = cursor.lastrowid

        order_query = "UPDATE orders SET status = %s, updated_at = %s WHERE id = %s"
        order_values = (OrderStatuses.PAID.value, datetime.now(), payment_data.order_id)
        cursor.execute(order_query, order_values)

        connection.commit()
        return {
            "info": "Payment created and order status updated",
            "payment_id": payment_id
        }

    except mysql.connector.errors.IntegrityError as e:
        connection.rollback()
        raise ValueError("The order does not exist or you do not have permission.")

    except Exception as e:
        connection.rollback()
        raise e

    finally:
        cursor.close()
        connection.close()


def update_order_status(order_id: int, new_status: OrderStatuses, user_id: int):
    connection = mysql_connection()
    try:
        connection.start_transaction()
        print(f"Updating status for order {order_id} to {new_status}")
        
        if not is_order_in_company(order_id, user_id):
            print(f"Order {order_id} is not in company for user {user_id}")
            connection.rollback()
            return {"error": "Order not in company"}

        cursor = connection.cursor(buffered=True)
        order_query = "UPDATE orders SET status = %s, updated_at = %s WHERE id = %s"
        order_values = (new_status.value, datetime.now(), order_id)
        print("Updating order status - Query Params:", new_status.value, order_id)
        cursor.execute(order_query, order_values)
        cursor.execute(order_query, order_values)
        
        if cursor.rowcount == 0:
            print(f"Order {order_id} not found")
            connection.rollback()
            return {"error": "Order not found"}

        connection.commit()
        print(f"Order status updated for order {order_id}")
        return {"info": "Order status updated", "order_id": order_id}
    except Exception as e:
        print(f"Error updating order status: {e}")
        connection.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.disconnect()


def update_payment_status(payment_id: int, new_status: PaymentStatuses):
    connection = mysql_connection()
    
    try:
        connection.start_transaction()
        cursor = connection.cursor(buffered=True)
        
        query = "UPDATE payments SET payment_status = %s, updated_at = %s WHERE id = %s"
        updated_at = datetime.now()
        cursor.execute(query, (new_status.value, updated_at, payment_id))

        if cursor.rowcount == 0:
            connection.rollback()
            raise ValueError(f"No payment found with payment_id {payment_id}")

        connection.commit()
        return {"info": "Payment status updated", "payment_id": payment_id}
    except Exception as e:
        if connection.in_transaction:
            connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def generate_receipt(order, payment):
    vat_included = order.total_price / (1 + VAT_RATE)
    vat_amount = round(order.total_price - vat_included,2)
    

    discount_amount = round(order.total_price * (payment.discount_percentage / 100), 2)
    final_amount = round(order.total_price - discount_amount + payment.tip, 2)
    change_given = round(payment.amount - final_amount, 2) if payment.amount > final_amount else 0

    if payment.payment_method == PaymentMethod.CASH and payment.amount > final_amount:
        change_given = round(payment.amount - final_amount, 2)
    else:
        change_given = 0

    receipt = {
        "order_id": order.id,
        "subtotal": vat_included,  
        "vat_rate": VAT_RATE,
        "vat_amount": vat_amount,  
        "discount": discount_amount,
        "tip": payment.tip,
        "total_due": final_amount,  
        "change_given": change_given  

    }
    
    return receipt


def get_order_for_payment(order_id: int, user_id: int) -> OrderModel | None:
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
            item_query = "SELECT item_id, quantity FROM order_item WHERE order_id = %s"
            cursor_order_item.execute(item_query, (order_id,))
            order_items = cursor_order_item.fetchall()
            
            products = [item[0] for item in order_items]
            quantities = [item[1] for item in order_items]

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
            not_found_status = OrderStatuses.NOT_FOUND  
            return OrderModel(
                id=0,  
                user_id=user_id,
                assignee_id=None,
                company_id=0,  
                products=[],
                quantities=[],
                total_price=0.0,
                created_at=datetime.now(),
                updated_at=None,
                status=not_found_status
            )
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor_orders.close()
        cursor_order_item.close()
        connection.disconnect()
        connection.close()


def run_transaction_with_retry(func, max_retries=5):
    attempt = 0
    while attempt < max_retries:
        try:
            return func()
        except mysql.connector.errors.OperationalError as e:
            if 'Lock wait timeout exceeded' in str(e):
                wait = 2 ** attempt
                print(f"Waiting for {wait} seconds before retrying...")
                time.sleep(wait)
                attempt += 1
            else:
                raise
    raise Exception("Transaction failed after retries")


def calculate_total_due(order, payment):
    discount = round(order.total_price * payment.discount_percentage / 100, 2) if payment.discount_percentage > 0 else 0
    
    total_due = order.total_price - discount

    total_due += payment.tip if payment.tip > 0 else 0

    tax = round(total_due - (total_due / (1 + VAT_RATE)), 2)

    change = 0.0

    return total_due, tax, discount


def get_payment_details(payment_id: int) -> Optional[PaymentModel]:
    connection = mysql_connection()
    try:
        cursor = connection.cursor()
        query = "SELECT order_id, user_id, amount, tip, payment_method, payment_status, discount_percentage FROM payments WHERE id = %s"
        cursor.execute(query, (payment_id,))
        payment_data = cursor.fetchone()
        if payment_data:
            payment_method = str(payment_data[4]) if payment_data[4] else None
            payment_status = int(payment_data[5]) if payment_data[5] else None
            discount_percentage = float(payment_data[6]) if payment_data[6] is not None else 0.0

            return PaymentModel(
                order_id=payment_data[0],
                user_id=payment_data[1],
                amount=float(payment_data[2]),  
                tip=float(payment_data[3]),  
                payment_method=payment_method,
                payment_status=payment_status,
                discount_percentage=discount_percentage,
            )
        return None
    except mysql.connector.Error as err:
        print("Error: ", err)
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

