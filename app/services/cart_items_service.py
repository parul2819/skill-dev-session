from fastapi import HTTPException, status

from app.dto.cart_items_dto import CartItemCreate, CartItemUpdate
from app.orm.cart_items import CartItem
from app.repositories.cart_items_repository import CartItemRepository


class CartItemService:
    def __init__(self, repo: CartItemRepository) -> None:
        self.repo = repo

    def list_cart_items(self) -> list[CartItem]:
        return self.repo.list_active()

    def get_cart_item(self, item_id: int) -> CartItem:
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        return item

    def create_cart_item(self, payload: CartItemCreate) -> CartItem:
        item = CartItem(
            cart_id=payload.cart_id,
            item_id=payload.item_id,
            quantity=payload.quantity,
            created_by=payload.created_by,
        )
        return self.repo.create(item)

    def update_cart_item(self, item_id: int, payload: CartItemUpdate) -> CartItem:
        item = self.get_cart_item(item_id)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        return self.repo.update(item)

    def delete_cart_item(self, item_id: int) -> None:
        item = self.get_cart_item(item_id)
        self.repo.soft_delete(item)