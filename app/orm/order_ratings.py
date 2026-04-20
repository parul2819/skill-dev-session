from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, Text, TIMESTAMP, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.base import Base


class OrderRatingOrm(Base):
    __tablename__ = "order_ratings"
    __table_args__ = (
        UniqueConstraint("order_id", name="order_ratings_order_id_key"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="order_ratings_rating_check"),
    )

    rating_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.restaurant_id"), nullable=False)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    review: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
