from fastapi import HTTPException, status
from app.dto import OrderRatingCreate, OrderRatingUpdate
from app.orm import OrderRatingOrm
from app.repositories import OrderRatingRepository


class OrderRatingService:
    def __init__(self, repo: OrderRatingRepository) -> None:
        self.repo = repo

    async def list_ratings(self) -> list[OrderRatingOrm]:
        return await self.repo.list_active()

    async def get_rating(self, rating_id: int) -> OrderRatingOrm:
        rating = await self.repo.get_by_id(rating_id)
        if not rating:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
        return rating

    async def create_rating(self, payload: OrderRatingCreate) -> OrderRatingOrm:
        # Check if rating already exists for the order
        existing = await self.repo.get_by_order_id(payload.order_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Rating already exists for this order")

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
