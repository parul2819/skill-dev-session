from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.orm.base import AuditMixin


class MenuItemOrm(Base, AuditMixin):
    __tablename__ = "menu_items"

    item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.restaurant_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    is_veg: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    is_available: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    restaurant = relationship("RestaurantOrm", back_populates="menu_items")
    order_items = relationship("OrderItemOrm", back_populates="menu_item")
    cart_items = relationship("CartItemOrm", back_populates="menu_item")
    