from fastapi import HTTPException, status
from app.dto.order_ratings_dto import OrderRatingCreate, OrderRatingUpdate
from app.orm.order_ratings import OrderRating
from app.repositories.order_ratings_repository import OrderRatingRepository


class OrderRatingService:
    def __init__(self, repo: OrderRatingRepository) -> None:
        self.repo = repo

    def list_ratings(self) -> list[OrderRating]:
        return self.repo.list_active()

    def get_rating(self, rating_id: int) -> OrderRating:
        rating = self.repo.get_by_id(rating_id)
        if not rating:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
        return rating

    def create_rating(self, payload: OrderRatingCreate) -> OrderRating:
        # Check if rating already exists for the order
        existing = self.repo.get_by_order_id(payload.order_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Rating already exists for this order")

        order_rating = OrderRating(
            order_id=payload.order_id,
            user_id=payload.user_id,
            restaurant_id=payload.restaurant_id,
            rating=payload.rating,
            review=payload.review,
        )
        return self.repo.create(order_rating)

    def update_rating(self, rating_id: int, payload: OrderRatingUpdate) -> OrderRating:
        order_rating = self.get_rating(rating_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order_rating, key, value)
        return self.repo.update(order_rating)

    def delete_rating(self, rating_id: int) -> None:
        order_rating = self.get_rating(rating_id)
        self.repo.soft_delete(order_rating)
