from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.orm import UserAddressOrm


class UserAddressRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[UserAddressOrm]:
        stmt = select(UserAddressOrm).where(UserAddressOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, address_id: int) -> UserAddressOrm | None:
        stmt = select(UserAddressOrm).where(
            UserAddressOrm.address_id == address_id,
            UserAddressOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_user_id(self, user_id: int) -> list[UserAddressOrm]:
        stmt = select(UserAddressOrm).where(
            UserAddressOrm.user_id == user_id,
            UserAddressOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def reset_default_for_user(self, user_id: int) -> None:
        stmt = (
            update(UserAddressOrm)
            .where(UserAddressOrm.user_id == user_id, UserAddressOrm.is_default.is_(True))
            .values(is_default=False)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def create(self, user_address: UserAddressOrm) -> UserAddressOrm:
        self.db.add(user_address)
        await self.db.commit()
        await self.db.refresh(user_address)
        return user_address

    async def update(self, user_address: UserAddressOrm) -> UserAddressOrm:
        self.db.add(user_address)
        await self.db.commit()
        await self.db.refresh(user_address)
        return user_address

    async def soft_delete(self, user_address: UserAddressOrm) -> None:
        user_address.is_deleted = True
        self.db.add(user_address)
        await self.db.commit()
