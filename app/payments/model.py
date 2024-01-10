from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import List, Optional

VAT_RATE = 0.21  
CURRENCY = "EUR"

class PaymentStatuses(Enum):
    PENDING = 1
    COMPLETED = 2
    VOIDED = 3
    REFUNDED = 4

class PaymentMethod(str, Enum):
    CASH = 'CASH'
    CARD = 'CARD'

class ReceiptItemModel(BaseModel):
    item_id: int
    quantity: int
    price: float

class ReceiptModel(BaseModel):
    order_id: int
    subtotal: float
    vat_rate: float
    vat_amount: float
    discount: float
    tip: float
    total_due: float

class PaymentModel(BaseModel):
    order_id: int
    user_id: Optional[int] = None 
    amount: float
    discount_percentage: Optional[float] = Field(0.0, ge=0.0, le=100.0)
    tip: float = Field(default=0.0)
    payment_method: PaymentMethod
    payment_status: PaymentStatuses = Field(default=PaymentStatuses.PENDING)



    @validator('payment_method', pre=True, allow_reuse=True)
    def parse_payment_method(cls, value):
        if isinstance(value, str):
            value = value.upper()  
        else:
            raise ValueError(f"Invalid type for payment_method, expected a string but got {type(value).__name__}")
        try:
            return PaymentMethod[value]
        except KeyError:
            raise ValueError(f"Value error, '{value}' is not a valid PaymentMethod")

    class Config:
        use_enum_values = True
        from_attributes = True  
        json_schema_extra = {   
            "example": {
                "order_id": 1,
                "amount": 100.00,
                "tip": 10.00,
                "payment_method": "CASH",
                "discount_percentage": 10 
            }
        }


