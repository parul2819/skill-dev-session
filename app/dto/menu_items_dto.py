from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MenuItemCreate(BaseModel):
    restaurant_id: int
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    is_veg: bool | None = None
    is_available: bool | None = None


class MenuItemUpdate(BaseModel):
    restaurant_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    is_veg: bool | None = None
    is_available: bool | None = None


class MenuItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: int
    restaurant_id: int
    name: str
    description: str | None
    price: float
    is_veg: bool | None
    is_available: bool | None
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
    is_deleted: bool
