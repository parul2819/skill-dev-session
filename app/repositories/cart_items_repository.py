from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import CartItemOrm


class CartItemRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[CartItemOrm]:
        stmt = select(CartItemOrm).where(CartItemOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, item_id: int) -> CartItemOrm | None:
        stmt = select(CartItemOrm).where(
            CartItemOrm.item_id == item_id,
            CartItemOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, item: CartItemOrm) -> CartItemOrm:
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item: CartItemOrm) -> CartItemOrm:
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def soft_delete(self, item: CartItemOrm) -> None:
        item.is_deleted = True
        self.db.add(item)
        await self.db.commit()
