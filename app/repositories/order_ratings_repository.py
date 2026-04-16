from sqlalchemy import select
from sqlalchemy.orm import Session
from app.orm.order_ratings import OrderRating

class OrderRatingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[OrderRating]:
        stmt = select(OrderRating).where(OrderRating.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, rating_id: int) -> OrderRating | None:
        stmt = select(OrderRating).where(
            OrderRating.rating_id == rating_id,
            OrderRating.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def get_by_order_id(self, order_id: int) -> OrderRating | None:
        stmt = select(OrderRating).where(
            OrderRating.order_id == order_id,
            OrderRating.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def get_by_restaurant_id(self, restaurant_id: int) -> list[OrderRating]:
        stmt = select(OrderRating).where(
            OrderRating.restaurant_id == restaurant_id,
            OrderRating.is_deleted.is_(False),
        )
        return list(self.db.scalars(stmt).all())

    def create(self, order_rating: OrderRating) -> OrderRating:
        self.db.add(order_rating)
        self.db.commit()
        self.db.refresh(order_rating)
        return order_rating

    def update(self, order_rating: OrderRating) -> OrderRating:
        self.db.add(order_rating)
        self.db.commit()
        self.db.refresh(order_rating)
        return order_rating

    def soft_delete(self, order_rating: OrderRating) -> None:
        order_rating.is_deleted = True
        self.db.add(order_rating)
        self.db.commit()
