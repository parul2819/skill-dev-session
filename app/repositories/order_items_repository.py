from sqlalchemy import select
from sqlalchemy.orm import Session
from app.orm.order_items import OrderItem

class OrderItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[OrderItem]:
        stmt = select(OrderItem).where(OrderItem.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, order_item_id: int) -> OrderItem | None:
        stmt = select(OrderItem).where(
            OrderItem.order_item_id == order_item_id,
            OrderItem.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def get_by_order_id(self, order_id: int) -> list[OrderItem]:
        stmt = select(OrderItem).where(
            OrderItem.order_id == order_id,
            OrderItem.is_deleted.is_(False),
        )
        return list(self.db.scalars(stmt).all())

    def create(self, order_item: OrderItem) -> OrderItem:
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        return order_item

    def update(self, order_item: OrderItem) -> OrderItem:
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        return order_item

    def soft_delete(self, order_item: OrderItem) -> None:
        order_item.is_deleted = True
        self.db.add(order_item)
        self.db.commit()
