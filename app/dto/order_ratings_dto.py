from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class OrderRatingCreate(BaseModel):
    order_id: int
    user_id: int
    restaurant_id: int
    rating: int | None = Field(default=None, ge=1, le=5)
    review: str | None = None


class OrderRatingUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    review: str | None = None


class OrderRatingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rating_id: int
    order_id: int
    user_id: int
    restaurant_id: int
    rating: int | None
    review: str | None
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
    is_deleted: bool
