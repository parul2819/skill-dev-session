from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.orm.base import AuditMixin


class CartItemOrm(Base, AuditMixin):
    __tablename__ = "cart_items"

    cart_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.cart_id"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.item_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    cart = relationship("CartOrm", back_populates="items")
    menu_item = relationship("MenuItemOrm", back_populates="cart_items")
    