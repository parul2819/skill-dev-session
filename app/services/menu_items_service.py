from fastapi import HTTPException, status

from app.dto import MenuItemCreate, MenuItemUpdate
from app.orm import MenuItemOrm
from app.repositories import MenuItemRepository


class MenuItemService:
    def __init__(self, repo: MenuItemRepository) -> None:
        self.repo = repo

    async def list_menu_items(self) -> list[MenuItemOrm]:
        return await self.repo.list_active()

    async def get_menu_item(self, item_id: int) -> MenuItemOrm:
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
        return item

    async def create_menu_item(self, payload: MenuItemCreate) -> MenuItemOrm:
        item = MenuItemOrm(
            restaurant_id=payload.restaurant_id,
            name=payload.name,
            description=payload.description,
            price=payload.price,
            is_veg=payload.is_veg,
            is_available=payload.is_available,
        )
        return await self.repo.create(item)

    async def update_menu_item(self, item_id: int, payload: MenuItemUpdate) -> MenuItemOrm:
        item = await self.get_menu_item(item_id)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        return await self.repo.update(item)

    async def delete_menu_item(self, item_id: int) -> None:
        item = await self.get_menu_item(item_id)
        await self.repo.soft_delete(item)
