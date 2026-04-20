from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import CartOrm


class CartRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[CartOrm]:
        stmt = select(CartOrm).where(CartOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, cart_id: int) -> CartOrm | None:
        stmt = select(CartOrm).where(
            CartOrm.cart_id == cart_id,
            CartOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_user_id(self, user_id: int) -> CartOrm | None:
        stmt = select(CartOrm).where(
            CartOrm.user_id == user_id,
            CartOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, cart: CartOrm) -> CartOrm:
        self.db.add(cart)
        await self.db.commit()
        await self.db.refresh(cart)
        return cart

    async def update(self, cart: CartOrm) -> CartOrm:
        self.db.add(cart)
        await self.db.commit()
        await self.db.refresh(cart)
        return cart

    async def soft_delete(self, cart: CartOrm) -> None:
        cart.is_deleted = True
        self.db.add(cart)
        await self.db.commit()
