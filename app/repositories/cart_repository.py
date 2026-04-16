from sqlalchemy import select
from sqlalchemy.orm import Session

from app.orm.cart import Cart


class CartRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[Cart]:
        stmt = select(Cart).where(Cart.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, cart_id: int) -> Cart | None:
        stmt = select(Cart).where(
            Cart.cart_id == cart_id,
            Cart.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def get_by_user_id(self, user_id: int) -> Cart | None:
        stmt = select(Cart).where(
            Cart.user_id == user_id,
            Cart.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def create(self, cart: Cart) -> Cart:
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def update(self, cart: Cart) -> Cart:
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def soft_delete(self, cart: Cart) -> None:
        cart.is_deleted = True
        self.db.add(cart)
        self.db.commit()
