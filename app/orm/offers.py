from sqlalchemy import Boolean, Enum, Integer, Numeric, String, Text, Date, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.enums import DiscountTypeEnum
from app.core.db.base import Base


class Offer(Base):
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
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
