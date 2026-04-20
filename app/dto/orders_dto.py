from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.common.enums import OrderStatusEnum


class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    offer_id: int | None = None
    total_amount: float = Field(ge=0)
    discount_amount: float | None = Field(default=None, ge=0)
    final_amount: float = Field(ge=0)
    order_status: OrderStatusEnum = OrderStatusEnum.pending


class OrderUpdate(BaseModel):
    user_id: int | None = None
    restaurant_id: int | None = None
    offer_id: int | None = None
    total_amount: float | None = Field(default=None, ge=0)
    discount_amount: float | None = Field(default=None, ge=0)
    final_amount: float | None = Field(default=None, ge=0)
    order_status: OrderStatusEnum | None = None


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    user_id: int
    restaurant_id: int
    offer_id: int | None
    total_amount: float
    discount_amount: float | None
    final_amount: float
    order_status: OrderStatusEnum
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
    is_deleted: bool
