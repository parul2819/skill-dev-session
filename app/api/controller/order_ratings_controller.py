from fastapi import APIRouter, Depends, status
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.get_db import get_db
from app.dto import OrderRatingCreate, OrderRatingRead, OrderRatingUpdate
from app.repositories import OrderRatingRepository
from app.services import OrderRatingService

router = APIRouter(prefix="/order-ratings", tags=["Order Ratings"])


async def get_order_rating_service(db: AsyncSession = Depends(get_db)) -> Any:
    repo = OrderRatingRepository(db)
    return OrderRatingService(repo)


@router.get("/", response_model=list[OrderRatingRead])
async def list_ratings(service: OrderRatingService = Depends(get_order_rating_service)) -> Any:
    return await service.list_ratings()


@router.get("/{rating_id}", response_model=OrderRatingRead)
async def get_rating(rating_id: int, service: OrderRatingService = Depends(get_order_rating_service)) -> Any:
    return await service.get_rating(rating_id)


@router.post("/", response_model=OrderRatingRead, status_code=status.HTTP_201_CREATED)
async def create_rating(payload: OrderRatingCreate, service: OrderRatingService = Depends(get_order_rating_service)) -> Any:
    return await service.create_rating(payload)


@router.patch("/{rating_id}", response_model=OrderRatingRead)
async def update_rating(
    rating_id: int, payload: OrderRatingUpdate, service: OrderRatingService = Depends(get_order_rating_service)
) -> Any:
    return await service.update_rating(rating_id, payload)


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rating(rating_id: int, service: OrderRatingService = Depends(get_order_rating_service)) -> None:
    await service.delete_rating(rating_id)
