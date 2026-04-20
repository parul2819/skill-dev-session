from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.orm import OrderOrm


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[OrderOrm]:
        stmt = select(OrderOrm).where(OrderOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, order_id: int) -> OrderOrm | None:
        stmt = select(OrderOrm).where(
            OrderOrm.order_id == order_id,
            OrderOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_user_id(self, user_id: int) -> list[OrderOrm]:
        stmt = select(OrderOrm).where(
            OrderOrm.user_id == user_id,
            OrderOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def create(self, order: OrderOrm) -> OrderOrm:
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def update(self, order: OrderOrm) -> OrderOrm:
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def soft_delete(self, order: OrderOrm) -> None:
        order.is_deleted = True
        self.db.add(order)
        await self.db.commit()
