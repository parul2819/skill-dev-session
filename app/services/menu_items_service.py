from fastapi import HTTPException, status

from app.dto.menu_items_dto import MenuItemCreate, MenuItemUpdate
from app.orm.menu_items import MenuItem
from app.repositories.menu_items_repository import MenuItemRepository


class MenuItemService:
    def __init__(self, repo: MenuItemRepository) -> None:
        self.repo = repo

    def list_menu_items(self) -> list[MenuItem]:
        return self.repo.list_active()

    def get_menu_item(self, item_id: int) -> MenuItem:
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
        return item

    def create_menu_item(self, payload: MenuItemCreate) -> MenuItem:
        item = MenuItem(
            restaurant_id=payload.restaurant_id,
            name=payload.name,
            description=payload.description,
            price=payload.price,
            is_veg=payload.is_veg,
            is_available=payload.is_available,
        )
        return self.repo.create(item)

    def update_menu_item(self, item_id: int, payload: MenuItemUpdate) -> MenuItem:
        item = self.get_menu_item(item_id)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        return self.repo.update(item)

    def delete_menu_item(self, item_id: int) -> None:
        item = self.get_menu_item(item_id)
        self.repo.soft_delete(item)