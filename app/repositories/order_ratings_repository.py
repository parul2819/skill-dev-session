from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.orm import OrderRatingOrm


class OrderRatingRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[OrderRatingOrm]:
        stmt = select(OrderRatingOrm).where(OrderRatingOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, rating_id: int) -> OrderRatingOrm | None:
        stmt = select(OrderRatingOrm).where(
            OrderRatingOrm.rating_id == rating_id,
            OrderRatingOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_order_id(self, order_id: int) -> OrderRatingOrm | None:
        stmt = select(OrderRatingOrm).where(
            OrderRatingOrm.order_id == order_id,
            OrderRatingOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_restaurant_id(self, restaurant_id: int) -> list[OrderRatingOrm]:
        stmt = select(OrderRatingOrm).where(
            OrderRatingOrm.restaurant_id == restaurant_id,
            OrderRatingOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def create(self, order_rating: OrderRatingOrm) -> OrderRatingOrm:
        self.db.add(order_rating)
        await self.db.commit()
        await self.db.refresh(order_rating)
        return order_rating

    async def update(self, order_rating: OrderRatingOrm) -> OrderRatingOrm:
        self.db.add(order_rating)
        await self.db.commit()
        await self.db.refresh(order_rating)
        return order_rating

    async def soft_delete(self, order_rating: OrderRatingOrm) -> None:
        order_rating.is_deleted = True
        self.db.add(order_rating)
        await self.db.commit()
