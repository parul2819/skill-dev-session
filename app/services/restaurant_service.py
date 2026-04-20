from fastapi import HTTPException, status

from app.dto import RestaurantCreate, RestaurantUpdate
from app.orm import RestaurantOrm
from app.repositories import RestaurantRepository


class RestaurantService:
    def __init__(self, repo: RestaurantRepository) -> None:
        self.repo = repo

    async def list_restaurants(self) -> list[RestaurantOrm]:
        return await self.repo.list_active()

    async def get_restaurant(self, restaurant_id: int) -> RestaurantOrm:
        restaurant = await self.repo.get_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        return restaurant

    async def create_restaurant(self, payload: RestaurantCreate) -> RestaurantOrm:
        restaurant = RestaurantOrm(
            name=payload.name,
            address=payload.address,
            phone_number=payload.phone_number,
            status=payload.status,
        )
        return await self.repo.create(restaurant)

    async def update_restaurant(self, restaurant_id: int, payload: RestaurantUpdate) -> RestaurantOrm:
        restaurant = await self.get_restaurant(restaurant_id)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(restaurant, key, value)

        return await self.repo.update(restaurant)

    async def delete_restaurant(self, restaurant_id: int) -> None:
        restaurant = await self.get_restaurant(restaurant_id)
        await self.repo.soft_delete(restaurant)
