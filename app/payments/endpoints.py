import fastapi
from fastapi import Depends, Path, HTTPException
import mysqlx
from app.db_connection import mysql_connection
from app.orders.model import OrderStatuses
from app.payments.model import CURRENCY, VAT_RATE, PaymentMethod, PaymentModel, PaymentStatuses, ReceiptModel
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
import app.payments.db as db
from app.orders.db import  update_order_status
from app.payments.db import calculate_total_due, create_payment, generate_receipt, get_order_for_payment, get_payment_details, update_payment_status
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
from app.JWT_auth.user_identification import UserIdentification
import app.users.check as users_check


router = fastapi.APIRouter()

@router.post("/cinematic/payments", tags=["payments"], status_code=201)
async def accept_payment(payment: PaymentModel, user_identification: UserIdentification = fastapi.Depends(authorization_wrapper)):
    try:
        connection = mysql_connection()
        connection.start_transaction()
        
        order = get_order_for_payment(payment.order_id, user_identification.id)
        if not order:
            raise fastapi.HTTPException(status_code=404, detail="Order not found.")
            
        if order.status == OrderStatuses.PAID:
            raise fastapi.HTTPException(status_code=400, detail="Order is already paid.")

        discount_amount = round(order.total_price * (payment.discount_percentage / 100.0), 2)
        total_due, tax, discount = calculate_total_due(order, payment)

        if payment.amount < total_due:
            raise fastapi.HTTPException(status_code=400, detail="Insufficient payment amount")

        if payment.payment_method == PaymentMethod.CARD:
            charged_amount = total_due + payment.tip - discount_amount
            change = 0.0

            payment.amount = charged_amount  
        else:
            change = max(payment.amount - total_due, 0.0)

        change = round(max(payment.amount - total_due, 0.0), 2)

        result = create_payment(payment, user_identification.id)
        actual_payment_id = result['payment_id']

        update_payment_status(actual_payment_id, PaymentStatuses.COMPLETED)
        update_order_status(payment.order_id, OrderStatuses.PAID, user_identification.id)

        connection.commit()

        return {
            "info": "Payment processed",
            "payment_id": actual_payment_id,
            "discount": discount_amount,
            "change": change,
            "card_payment_confirmation": f"Payment of {total_due} {CURRENCY} successful" if payment.payment_method == PaymentMethod.CARD else None
        }

    except fastapi.HTTPException as http_exc:
        if connection:
            connection.rollback()
        raise http_exc
    except Exception as e:
        if connection:
            connection.rollback()
        raise fastapi.HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            connection.close()


@router.get("/cinematic/payments/{payment_id}/receipts", response_model=ReceiptModel)
async def generate_receipts(
    payment_id: int = Path(..., description="The ID of the payment"),
    user_identification: UserIdentification = Depends(authorization_wrapper)
):
    payment = get_payment_details(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    order = get_order_for_payment(payment.order_id, user_identification.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    vat_included = order.total_price / (1 + VAT_RATE)
    vat_amount = order.total_price - vat_included
    discount_amount = (order.total_price * payment.discount_percentage) / 100 if payment.discount_percentage else 0

    final_amount = order.total_price - discount_amount + payment.tip   

    receipt = ReceiptModel(
        order_id=order.id,
        subtotal=vat_included,
        vat_rate=VAT_RATE,
        vat_amount=vat_amount,
        discount=discount_amount,
        tip=payment.tip,
        total_due=final_amount
    )
    return receipt


@router.post("/cinematic/payments/{payment_id}/refunds", tags=["payments"])
async def process_refund(
    payment_id: int = Path(..., description="The ID of the payment to refund"),
    user_identification: UserIdentification = Depends(authorization_wrapper)
):
    user_info = get_complete_user_information(user_identification.id)
    
    payment = get_payment_details(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.payment_status != PaymentStatuses.COMPLETED.value:
        raise HTTPException(status_code=400, detail="Only completed payments can be refunded")

    order = get_order_for_payment(payment.order_id, user_info.id)
    if not order or order.company_id != user_info.company_id:
        raise HTTPException(status_code=403, detail="Order not found or does not belong to the user's company")

    update_payment_status(payment_id, PaymentStatuses.REFUNDED)

    update_order_status(order.id, OrderStatuses.REFUNDED, user_info.id)

    return {"info": f"Refund processed for payment {payment_id}"}


@router.post("/cinematic/payments/{payment_id}/void", tags=["payments"])
async def void_payment(
    payment_id: int = Path(..., description="The ID of the payment to be voided"),
    user_identification: UserIdentification = Depends(authorization_wrapper)
):
    user_info = get_complete_user_information(user_identification.id)

    payment = get_payment_details(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.payment_status != PaymentStatuses.PENDING.value:
        raise HTTPException(status_code=400, detail="Only pending payments can be voided")

    update_payment_status(payment_id, PaymentStatuses.VOIDED)

    update_order_status(payment.order_id, OrderStatuses.VOIDED, user_info.id)

    return {"info": "Payment has been voided"}



