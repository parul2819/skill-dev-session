from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.orm.base import AuditMixin


class UserAddressOrm(Base, AuditMixin):
    __tablename__ = "user_addresses"
    __table_args__ = (
        Index(
            "unique_default_address_per_user",
            "user_id",
            unique=True,
            postgresql_where=text("is_default"),
        ),
    )

    address_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    address_line: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str | None] = mapped_column(String(50), nullable=True)
    state: Mapped[str | None] = mapped_column(String(50), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(10), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    user = relationship("UserOrm", back_populates="addresses")
