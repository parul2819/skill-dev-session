from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class UserAddressCreate(BaseModel):
    user_id: int
    address_line: str
    city: str | None = Field(default=None, max_length=50)
    state: str | None = Field(default=None, max_length=50)
    pincode: str | None = Field(default=None, max_length=10)
    is_default: bool = False

class UserAddressUpdate(BaseModel):
    user_id: int | None = None
    address_line: str | None = None
    city: str | None = Field(default=None, max_length=50)
    state: str | None = Field(default=None, max_length=50)
    pincode: str | None = Field(default=None, max_length=10)
    is_default: bool | None = None

class UserAddressRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    address_id: int
    user_id: int
    address_line: str
    city: str | None
    state: str | None
    pincode: str | None
    is_default: bool
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
    is_deleted: bool
