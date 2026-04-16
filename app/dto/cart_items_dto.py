from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CartItemCreate(BaseModel):
    cart_id: int
    item_id: int
    quantity: int = Field(gt=0)
    created_by: int | None = None


class CartItemUpdate(BaseModel):
    quantity: int | None = Field(default=None, gt=0)
    updated_by: int | None = None
    is_deleted: bool | None = None


class CartItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cart_item_id: int
    cart_id: int
    item_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime
    created_by: int | None = None
    updated_by: int | None = None
    is_deleted: bool