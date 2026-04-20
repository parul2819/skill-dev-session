from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.core.db.get_db import get_db
from app.dto import RestaurantCreate, RestaurantRead, RestaurantUpdate
from app.repositories import RestaurantRepository
from app.services import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


async def get_restaurant_service(db: AsyncSession = Depends(get_db)) -> Any:
    repo = RestaurantRepository(db)
    return RestaurantService(repo)


@router.get("/", response_model=list[RestaurantRead])
async def list_restaurants(service: RestaurantService = Depends(get_restaurant_service)) -> Any:
    return await service.list_restaurants()


@router.get("/{restaurant_id}", response_model=RestaurantRead)
async def get_restaurant(
    restaurant_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
) -> Any:
    return await service.get_restaurant(restaurant_id)


@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    payload: RestaurantCreate,
    service: RestaurantService = Depends(get_restaurant_service),
) -> Any:
    return await service.create_restaurant(payload)


@router.put("/{restaurant_id}", response_model=RestaurantRead)
async def update_restaurant(
    restaurant_id: int,
    payload: RestaurantUpdate,
    service: RestaurantService = Depends(get_restaurant_service),
) -> Any:
    return await service.update_restaurant(restaurant_id, payload)


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant(
    restaurant_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
) -> None:
    await service.delete_restaurant(restaurant_id)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
