from sqlalchemy import select
from sqlalchemy.orm import Session
from app.orm.orders import Order

class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[Order]:
        stmt = select(Order).where(Order.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, order_id: int) -> Order | None:
        stmt = select(Order).where(
            Order.order_id == order_id,
            Order.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def get_by_user_id(self, user_id: int) -> list[Order]:
        stmt = select(Order).where(
            Order.user_id == user_id,
            Order.is_deleted.is_(False),
        )
        return list(self.db.scalars(stmt).all())

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def soft_delete(self, order: Order) -> None:
        order.is_deleted = True
        self.db.add(order)
        self.db.commit()
