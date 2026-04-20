from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.orm import OrderItemOrm


class OrderItemRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[OrderItemOrm]:
        stmt = select(OrderItemOrm).where(OrderItemOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, order_item_id: int) -> OrderItemOrm | None:
        stmt = select(OrderItemOrm).where(
            OrderItemOrm.order_item_id == order_item_id,
            OrderItemOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_order_id(self, order_id: int) -> list[OrderItemOrm]:
        stmt = select(OrderItemOrm).where(
            OrderItemOrm.order_id == order_id,
            OrderItemOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def create(self, order_item: OrderItemOrm) -> OrderItemOrm:
        self.db.add(order_item)
        await self.db.commit()
        await self.db.refresh(order_item)
        return order_item

    async def update(self, order_item: OrderItemOrm) -> OrderItemOrm:
        self.db.add(order_item)
        await self.db.commit()
        await self.db.refresh(order_item)
        return order_item

    async def soft_delete(self, order_item: OrderItemOrm) -> None:
        order_item.is_deleted = True
        self.db.add(order_item)
        await self.db.commit()
