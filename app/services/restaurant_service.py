from fastapi import HTTPException, status

from app.dto.restaurant_dto import RestaurantCreate, RestaurantUpdate
from app.orm.restaurants import Restaurant
from app.repositories.restaurant_repository import RestaurantRepository


class RestaurantService:
    def __init__(self, repo: RestaurantRepository) -> None:
        self.repo = repo

    def list_restaurants(self) -> list[Restaurant]:
        return self.repo.list_active()

    def get_restaurant(self, restaurant_id: int) -> Restaurant:
        restaurant = self.repo.get_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        return restaurant

    def create_restaurant(self, payload: RestaurantCreate) -> Restaurant:
        restaurant = Restaurant(
            name=payload.name,
            address=payload.address,
            phone_number=payload.phone_number,
            status=payload.status,
        )
        return self.repo.create(restaurant)

    def update_restaurant(self, restaurant_id: int, payload: RestaurantUpdate) -> Restaurant:
        restaurant = self.get_restaurant(restaurant_id)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(restaurant, key, value)

        return self.repo.update(restaurant)

    def delete_restaurant(self, restaurant_id: int) -> None:
        restaurant = self.get_restaurant(restaurant_id)
        self.repo.soft_delete(restaurant)
