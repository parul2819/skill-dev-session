from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import RestaurantOrm


class RestaurantRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[RestaurantOrm]:
        stmt = select(RestaurantOrm).where(RestaurantOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, restaurant_id: int) -> RestaurantOrm | None:
        stmt = select(RestaurantOrm).where(
            RestaurantOrm.restaurant_id == restaurant_id,
            RestaurantOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, restaurant: RestaurantOrm) -> RestaurantOrm:
        self.db.add(restaurant)
        await self.db.commit()
        await self.db.refresh(restaurant)
        return restaurant

    async def update(self, restaurant: RestaurantOrm) -> RestaurantOrm:
        self.db.add(restaurant)
        await self.db.commit()
        await self.db.refresh(restaurant)
        return restaurant

    async def soft_delete(self, restaurant: RestaurantOrm) -> None:
        restaurant.is_deleted = True
        self.db.add(restaurant)
        await self.db.commit()
