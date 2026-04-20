from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.orm import UserOrm


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[UserOrm]:
        stmt = select(UserOrm).where(UserOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, user_id: int) -> UserOrm | None:
        stmt = select(UserOrm).where(UserOrm.user_id == user_id, UserOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt) 
        return result.first()

    async def get_by_email(self, email: str) -> UserOrm | None:
        stmt = select(UserOrm).where(UserOrm.email == email, UserOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, user: UserOrm) -> UserOrm:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: UserOrm) -> UserOrm:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def soft_delete(self, user: UserOrm) -> None:
        user.is_deleted = True
        self.db.add(user)
        await self.db.commit()
