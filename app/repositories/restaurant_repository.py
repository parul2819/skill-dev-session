from sqlalchemy import select
from sqlalchemy.orm import Session

from app.orm.restaurants import Restaurant


class RestaurantRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[Restaurant]:
        stmt = select(Restaurant).where(Restaurant.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        stmt = select(Restaurant).where(
            Restaurant.restaurant_id == restaurant_id,
            Restaurant.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def create(self, restaurant: Restaurant) -> Restaurant:
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def update(self, restaurant: Restaurant) -> Restaurant:
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def soft_delete(self, restaurant: Restaurant) -> None:
        restaurant.is_deleted = True
        self.db.add(restaurant)
        self.db.commit()
