from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.base import Base
from app.orm.base import AuditMixin


class UserOrm(Base, AuditMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True) #new column

    addresses = relationship("UserAddressOrm", back_populates="user")
    carts = relationship("CartOrm", back_populates="user")
    orders = relationship("OrderOrm", back_populates="user")
    ratings = relationship("OrderRatingOrm", back_populates="user")
