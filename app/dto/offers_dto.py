from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import DiscountTypeEnum


class OfferCreate(BaseModel):
    code: str
    description: str | None = None
    discount_type: DiscountTypeEnum | None = None
    discount_value: float | None = Field(default=None, ge=0)
    min_order_amount: float | None = Field(default=None, ge=0)
    max_discount_amount: float | None = Field(default=None, ge=0)
    valid_from: date | None = None
    valid_to: date | None = None
    is_active: bool | None = None


class OfferUpdate(BaseModel):
    code: str | None = None
    description: str | None = None
    discount_type: DiscountTypeEnum | None = None
    discount_value: float | None = Field(default=None, ge=0)
    min_order_amount: float | None = Field(default=None, ge=0)
    max_discount_amount: float | None = Field(default=None, ge=0)
    valid_from: date | None = None
    valid_to: date | None = None
    is_active: bool | None = None


class OfferRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    offer_id: int
    code: str
    description: str | None
    discount_type: DiscountTypeEnum | None
    discount_value: float | None
    min_order_amount: float | None
    max_discount_amount: float | None
    valid_from: date | None
    valid_to: date | None
    is_active: bool | None
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
    is_deleted: bool
