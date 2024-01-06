import fastapi
from app.JWT_auth.user_identification import UserIdentification
from app.JWT_auth.authorization import authorization_wrapper
from app.orders.model import AddOrderItemModel, OrderPostModel, OrderStatuses, OrderUpdateModel
import app.orders.db as db
from app.db_error_handler import handle_db_error

router = fastapi.APIRouter()

@router.post("/cinematic/orders", tags=["orders"], status_code=201)
@handle_db_error
async def create_order(new_order : OrderPostModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.post_order(new_order, user_identification.id)

@router.get("/cinematic/orders", tags=["orders"], status_code=200)
@handle_db_error
async def get_orders(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.get_orders(user_identification.id)

@router.get("/cinematic/orders/{order_id}", tags=["orders"], status_code=200)
@handle_db_error
async def get_order(order_id : int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.get_order(order_id, user_identification.id)

@router.put("/cinematic/orders/{order_id}", tags=["orders"], status_code=200)
@handle_db_error
async def update_order(order_id : int, new_order : OrderUpdateModel = fastapi.Body(default=None), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.update_order(order_id, new_order, user_identification.id)

@router.delete("/cinematic/orders/{order_id}", tags=["orders"], status_code=200)
@handle_db_error
async def delete_order(order_id : int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.delete_order(order_id, user_identification.id)

@router.put("/cinematic/orders/{order_id}/status", tags=["orders"], status_code=200)
@handle_db_error
async def update_order_status(order_id : int, new_status : OrderStatuses = fastapi.Body(OrderStatuses.CONFIRMED), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.update_order_status(order_id, new_status, user_identification.id)

@router.post("/cinematic/orders/{order_id}/assign", tags=["orders"], status_code=201)
@handle_db_error
async def assign_order(order_id : int, assignee_id : int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.assign_order(order_id, assignee_id, user_identification.id)


@router.post("/cinematic/orders/{order_id}/addOrderItems", tags=["orders"], status_code=201)
@handle_db_error
async def add_order_item(order_item: AddOrderItemModel, order_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.add_order_item(order_id, order_item, user_identification.id)


@router.delete("/cinematic/orders/{order_id}/deleteOrderItems", tags=["orders"], status_code=200)
@handle_db_error
async def delete_order_item(order_id: int, order_item_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.delete_order_item(order_id, order_item_id, user_identification.id)


@router.get("/cinematic/orders/{unassigned}/orderItems", tags=["orders"], status_code=200)
@handle_db_error
async def get_order_items(unassigned: bool, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.get_order_items(unassigned, user_identification.id)


@router.get("/cinematic/orders/orderItems/{order_item_id}", tags=["orders"], status_code=200)
@handle_db_error
async def get_order_item(order_item_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.get_order_item(order_item_id, user_identification.id)


@router.put("/cinematic/orders/orderItems/{order_item_id}/status", tags=["orders"], status_code=200)
@handle_db_error
async def update_order_item_status(order_item_id: int, new_status: OrderStatuses = fastapi.Body(OrderStatuses.CONFIRMED), user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.update_order_item_status(order_item_id, new_status, user_identification.id)


@router.put("/cinematic/orders/orderItems/{order_item_id}/assign", tags=["orders"], status_code=200)
@handle_db_error
async def assign_order_item(order_item_id: int, assignee_id: int, user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    return db.assign_order_item(order_item_id, assignee_id, user_identification.id)

