from sqlalchemy import Boolean, Enum, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.enums import RestaurantStatusEnum
from app.core.db.base import Base


class Restaurant(Base):
    __tablename__ = "restaurants"
    
    restaurant_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
    status: Mapped[RestaurantStatusEnum] = mapped_column(
        Enum(RestaurantStatusEnum, name="restaurant_status_enum"),
        default=RestaurantStatusEnum.active,
        nullable=False,
    )
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)