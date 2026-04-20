from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import OfferOrm


class OfferRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(self) -> list[OfferOrm]:
        stmt = select(OfferOrm).where(OfferOrm.is_deleted.is_(False))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, offer_id: int) -> OfferOrm | None:
        stmt = select(OfferOrm).where(
            OfferOrm.offer_id == offer_id,
            OfferOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def get_by_code(self, code: str) -> OfferOrm | None:
        stmt = select(OfferOrm).where(
            OfferOrm.code == code,
            OfferOrm.is_deleted.is_(False),
        )
        result = await self.db.scalars(stmt)
        return result.first()

    async def create(self, offer: OfferOrm) -> OfferOrm:
        self.db.add(offer)
        await self.db.commit()
        await self.db.refresh(offer)
        return offer

    async def update(self, offer: OfferOrm) -> OfferOrm:
        self.db.add(offer)
        await self.db.commit()
        await self.db.refresh(offer)
        return offer

    async def soft_delete(self, offer: OfferOrm) -> None:
        offer.is_deleted = True
        self.db.add(offer)
        await self.db.commit()
