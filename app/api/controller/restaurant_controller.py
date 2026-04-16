from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.db.get_db import get_db
from app.dto.restaurant_dto import RestaurantCreate, RestaurantRead, RestaurantUpdate
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.restaurant_service import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


def get_restaurant_service(db: Session = Depends(get_db)) -> RestaurantService:
    repo = RestaurantRepository(db)
    return RestaurantService(repo)


@router.get("/", response_model=list[RestaurantRead])
def list_restaurants(service: RestaurantService = Depends(get_restaurant_service)) -> list[RestaurantRead]:
    return service.list_restaurants()


@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(
    restaurant_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
) -> RestaurantRead:
    return service.get_restaurant(restaurant_id)


@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    payload: RestaurantCreate,
    service: RestaurantService = Depends(get_restaurant_service),
) -> RestaurantRead:
    return service.create_restaurant(payload)


@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    payload: RestaurantUpdate,
    service: RestaurantService = Depends(get_restaurant_service),
) -> RestaurantRead:
    return service.update_restaurant(restaurant_id, payload)


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
) -> Response:
    service.delete_restaurant(restaurant_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)