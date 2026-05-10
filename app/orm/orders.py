from sqlalchemy import Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.enums import OrderStatusEnum
from app.core.db.base import Base
from app.orm.base import AuditMixin


class OrderOrm(Base, AuditMixin):
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

    user = relationship("UserOrm", back_populates="orders")
    restaurant = relationship("RestaurantOrm", back_populates="orders")
    offer = relationship("OfferOrm", back_populates="orders")
    items = relationship("OrderItemOrm", back_populates="order")
    rating = relationship("OrderRatingOrm", back_populates="order", uselist=False)
