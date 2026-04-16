from fastapi import HTTPException, status

from app.dto.offers_dto import OfferCreate, OfferUpdate
from app.orm.offers import Offer
from app.repositories.offers_repository import OfferRepository


class OfferService:
    def __init__(self, repo: OfferRepository) -> None:
        self.repo = repo

    def list_offers(self) -> list[Offer]:
        return self.repo.list_active()

    def get_offer(self, offer_id: int) -> Offer:
        offer = self.repo.get_by_id(offer_id)
        if not offer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
        return offer

    def create_offer(self, payload: OfferCreate) -> Offer:
        existing = self.repo.get_by_code(payload.code)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Offer code already exists")

        offer = Offer(
            code=payload.code,
            description=payload.description,
            discount_type=payload.discount_type,
            discount_value=payload.discount_value,
            min_order_amount=payload.min_order_amount,
            max_discount_amount=payload.max_discount_amount,
            valid_from=payload.valid_from,
            valid_to=payload.valid_to,
            is_active=payload.is_active,
        )
        return self.repo.create(offer)

    def update_offer(self, offer_id: int, payload: OfferUpdate) -> Offer:
        offer = self.get_offer(offer_id)

        if payload.code and payload.code != offer.code:
            existing = self.repo.get_by_code(payload.code)
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Offer code already exists")

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(offer, key, value)

        return self.repo.update(offer)

    def delete_offer(self, offer_id: int) -> None:
        offer = self.get_offer(offer_id)
        self.repo.soft_delete(offer)
