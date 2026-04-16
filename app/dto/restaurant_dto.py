from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.common.enums import RestaurantStatusEnum


class RestaurantCreate(BaseModel):
    name: str
    address: str | None = None
    phone_number: str | None = None
    status: RestaurantStatusEnum = RestaurantStatusEnum.active


class RestaurantUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone_number: str | None = None
    status: RestaurantStatusEnum | None = None


class RestaurantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    restaurant_id: int
    name: str
    address: str | None
    phone_number: str | None
    status: RestaurantStatusEnum
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
    is_deleted: bool
