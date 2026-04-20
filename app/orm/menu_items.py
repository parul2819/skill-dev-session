from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.base import Base


class MenuItemOrm(Base):
    __tablename__ = "menu_items"

    item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.restaurant_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    is_veg: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    is_available: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
