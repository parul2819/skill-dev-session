from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db.get_db import get_db
from app.dto.order_ratings_dto import OrderRatingCreate, OrderRatingRead, OrderRatingUpdate
from app.repositories.order_ratings_repository import OrderRatingRepository
from app.services.order_ratings_service import OrderRatingService

router = APIRouter(prefix="/order-ratings", tags=["Order Ratings"])


def get_order_rating_service(db: Session = Depends(get_db)) -> OrderRatingService:
    repo = OrderRatingRepository(db)
    return OrderRatingService(repo)


@router.get("/", response_model=list[OrderRatingRead])
def list_ratings(service: OrderRatingService = Depends(get_order_rating_service)):
    return service.list_ratings()


@router.get("/{rating_id}", response_model=OrderRatingRead)
def get_rating(rating_id: int, service: OrderRatingService = Depends(get_order_rating_service)):
    return service.get_rating(rating_id)


@router.post("/", response_model=OrderRatingRead, status_code=status.HTTP_201_CREATED)
def create_rating(payload: OrderRatingCreate, service: OrderRatingService = Depends(get_order_rating_service)):
    return service.create_rating(payload)


@router.patch("/{rating_id}", response_model=OrderRatingRead)
def update_rating(
    rating_id: int, payload: OrderRatingUpdate, service: OrderRatingService = Depends(get_order_rating_service)
):
    return service.update_rating(rating_id, payload)


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(rating_id: int, service: OrderRatingService = Depends(get_order_rating_service)):
    service.delete_rating(rating_id)
