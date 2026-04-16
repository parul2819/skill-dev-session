from sqlalchemy import select
from sqlalchemy.orm import Session

from app.orm.offers import Offer


class OfferRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[Offer]:
        stmt = select(Offer).where(Offer.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, offer_id: int) -> Offer | None:
        stmt = select(Offer).where(
            Offer.offer_id == offer_id,
            Offer.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def get_by_code(self, code: str) -> Offer | None:
        stmt = select(Offer).where(
            Offer.code == code,
            Offer.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def create(self, offer: Offer) -> Offer:
        self.db.add(offer)
        self.db.commit()
        self.db.refresh(offer)
        return offer

    def update(self, offer: Offer) -> Offer:
        self.db.add(offer)
        self.db.commit()
        self.db.refresh(offer)
        return offer

    def soft_delete(self, offer: Offer) -> None:
        offer.is_deleted = True
        self.db.add(offer)
        self.db.commit()
