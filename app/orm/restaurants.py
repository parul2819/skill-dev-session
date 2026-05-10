from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.enums import RestaurantStatusEnum
from app.core.db.base import Base
from app.orm.base import AuditMixin


class RestaurantOrm(Base, AuditMixin):
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

    menu_items = relationship("MenuItemOrm", back_populates="restaurant")
    carts = relationship("CartOrm", back_populates="restaurant")
    orders = relationship("OrderOrm", back_populates="restaurant")
    ratings = relationship("OrderRatingOrm", back_populates="restaurant")
    