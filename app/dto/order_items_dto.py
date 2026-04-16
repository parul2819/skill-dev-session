from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    order_id: int
    item_id: int
    quantity: int = Field(gt=0)
    price: float = Field(ge=0)


class OrderItemUpdate(BaseModel):
    order_id: int | None = None
    item_id: int | None = None
    quantity: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, ge=0)


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_item_id: int
    order_id: int
    item_id: int
    quantity: int
    price: float
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
    is_deleted: bool
