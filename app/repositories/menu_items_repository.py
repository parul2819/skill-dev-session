from sqlalchemy import select
from sqlalchemy.orm import Session

from app.orm.menu_items import MenuItem


class MenuItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[MenuItem]:
        stmt = select(MenuItem).where(MenuItem.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, item_id: int) -> MenuItem | None:
        stmt = select(MenuItem).where(
            MenuItem.item_id == item_id,
            MenuItem.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def create(self, item: MenuItem) -> MenuItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: MenuItem) -> MenuItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def soft_delete(self, item: MenuItem) -> None:
        item.is_deleted = True
        self.db.add(item)
        self.db.commit()