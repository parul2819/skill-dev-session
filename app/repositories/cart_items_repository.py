from sqlalchemy import select
from sqlalchemy.orm import Session

from app.orm.cart_items import CartItem


class CartItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[CartItem]:
        stmt = select(CartItem).where(CartItem.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, item_id: int) -> CartItem | None:
        stmt = select(CartItem).where(
            CartItem.item_id == item_id,
            CartItem.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def create(self, item: CartItem) -> CartItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: CartItem) -> CartItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def soft_delete(self, item: CartItem) -> None:
        item.is_deleted = True
        self.db.add(item)
        self.db.commit()