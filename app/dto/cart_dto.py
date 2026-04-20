from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CartCreate(BaseModel):
    user_id: int
    restaurant_id: int


class CartUpdate(BaseModel):
    user_id: int | None = None
    restaurant_id: int | None = None


class CartRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cart_id: int
    user_id: int
    restaurant_id: int
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
    is_deleted: bool
