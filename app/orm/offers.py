from sqlalchemy import Boolean, Enum, Integer, Numeric, String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.enums import DiscountTypeEnum
from app.core.db.base import Base
from app.orm.base import AuditMixin


class OfferOrm(Base, AuditMixin):
    __tablename__ = "offers"

    offer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    discount_type: Mapped[DiscountTypeEnum | None] = mapped_column(
        Enum(DiscountTypeEnum, name="discount_type_enum"),
        nullable=True,
    )
    discount_value: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    min_order_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    max_discount_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    valid_from: Mapped[str | None] = mapped_column(Date, nullable=True)
    valid_to: Mapped[str | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    orders = relationship("OrderOrm", back_populates="offer")
    