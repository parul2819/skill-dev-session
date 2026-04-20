from sqlalchemy import Boolean, Enum, ForeignKey, Integer, Numeric, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.enums import OrderStatusEnum
from app.core.db.base import Base


class OrderOrm(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.restaurant_id"), nullable=False)
    offer_id: Mapped[int | None] = mapped_column(ForeignKey("offers.offer_id"), nullable=True)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    discount_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    final_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    order_status: Mapped[OrderStatusEnum] = mapped_column(
        Enum(OrderStatusEnum, name="order_status_enum"),
        default=OrderStatusEnum.pending,
        nullable=False,
    )
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
