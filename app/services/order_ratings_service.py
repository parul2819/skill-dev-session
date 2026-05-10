from app.core.logger import setup_logger
from app.core.exceptions.custom_exceptions import NotFoundException, ConflictException
from app.dto import OrderRatingCreate, OrderRatingUpdate
from app.orm import OrderRatingOrm
from app.repositories import OrderRatingRepository

logger = setup_logger()

class OrderRatingService:
    def __init__(self, repo: OrderRatingRepository) -> None:
        self.repo = repo

    async def list_ratings(self) -> list[OrderRatingOrm]:
        return await self.repo.list_active()

    async def get_rating(self, rating_id: int) -> OrderRatingOrm:
        rating = await self.repo.get_by_id(rating_id)
        if not rating:
            logger.error(f"Rating not found with ID: {rating_id}")
            raise NotFoundException(message="Rating not found")
        return rating

    async def create_rating(self, payload: OrderRatingCreate) -> OrderRatingOrm:
        # Check if rating already exists for the order
        existing = await self.repo.get_by_order_id(payload.order_id)
        if existing:
            logger.error(f"Rating already exists for order ID: {payload.order_id}")
            raise ConflictException(message="Rating already exists for this order")

        order_rating = OrderRatingOrm(
            order_id=payload.order_id,
            user_id=payload.user_id,
            restaurant_id=payload.restaurant_id,
            rating=payload.rating,
            review=payload.review,
        )
        return await self.repo.create(order_rating)

    async def update_rating(self, rating_id: int, payload: OrderRatingUpdate) -> OrderRatingOrm:
        order_rating = await self.get_rating(rating_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order_rating, key, value)
        return await self.repo.update(order_rating)

    async def delete_rating(self, rating_id: int) -> None:
        order_rating = await self.get_rating(rating_id)
        await self.repo.soft_delete(order_rating)
