from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import MenuItemOrm


class MenuItemRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[MenuItemOrm]:
        stmt = select(MenuItemOrm).where(MenuItemOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, item_id: int) -> MenuItemOrm | None:
        stmt = select(MenuItemOrm).where(
            MenuItemOrm.item_id == item_id,
            MenuItemOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, item: MenuItemOrm) -> MenuItemOrm:
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item: MenuItemOrm) -> MenuItemOrm:
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def soft_delete(self, item: MenuItemOrm) -> None:
        item.is_deleted = True
        self.db.add(item)
        await self.db.commit()
