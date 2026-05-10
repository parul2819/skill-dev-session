from sqlalchemy import ForeignKey, Integer,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.orm.base import AuditMixin


class CartOrm(Base, AuditMixin):
    __tablename__ = "cart"
    __table_args__ = (UniqueConstraint("user_id", name="cart_user_id_key"),)

    cart_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.restaurant_id"), nullable=False)

    user = relationship("UserOrm", back_populates="carts")
    restaurant = relationship("RestaurantOrm", back_populates="carts")
    items = relationship("CartItemOrm", back_populates="cart")
   