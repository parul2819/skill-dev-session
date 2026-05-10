from sqlalchemy import CheckConstraint, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.orm.base import AuditMixin


class OrderRatingOrm(Base, AuditMixin):
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

    order = relationship("OrderOrm", back_populates="rating")
    user = relationship("UserOrm", back_populates="ratings")
    restaurant = relationship("RestaurantOrm", back_populates="ratings")
