from app.core.logger import setup_logger
from app.core.exceptions.custom_exceptions import NotFoundException, ConflictException
from app.dto import OfferCreate, OfferUpdate
from app.orm import OfferOrm
from app.repositories import OfferRepository

logger = setup_logger()

class OfferService:
    def __init__(self, repo: OfferRepository) -> None:
        self.repo = repo

    async def list_offers(self) -> list[OfferOrm]:
        return await self.repo.list_active()

    async def get_offer(self, offer_id: int) -> OfferOrm:
        offer = await self.repo.get_by_id(offer_id)
        if not offer:
            logger.error(f"Offer not found with ID: {offer_id}")
            raise NotFoundException(message="Offer not found")
        return offer

    async def create_offer(self, payload: OfferCreate) -> OfferOrm:
        existing = await self.repo.get_by_code(payload.code)
        if existing:
            logger.error(f"Offer code conflict: {payload.code} already exists")
            raise ConflictException(message="Offer code already exists")

        offer = OfferOrm(
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
        return await self.repo.create(offer)

    async def update_offer(self, offer_id: int, payload: OfferUpdate) -> OfferOrm:
        offer = await self.get_offer(offer_id)

        if payload.code and payload.code != offer.code:
            existing = await self.repo.get_by_code(payload.code)
            if existing:
                logger.error(f"Offer code conflict on update: {payload.code} already exists")
                raise ConflictException(message="Offer code already exists")

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(offer, key, value)

        return await self.repo.update(offer)

    async def delete_offer(self, offer_id: int) -> None:
        offer = await self.get_offer(offer_id)
        await self.repo.soft_delete(offer)
