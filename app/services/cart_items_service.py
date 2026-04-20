from fastapi import HTTPException, status

from app.dto import CartItemCreate, CartItemUpdate
from app.orm import CartItemOrm
from app.repositories import CartItemRepository


class CartItemService:
    def __init__(self, repo: CartItemRepository) -> None:
        self.repo = repo

    async def list_cart_items(self) -> list[CartItemOrm]:
        return await self.repo.list_active()

    async def get_cart_item(self, item_id: int) -> CartItemOrm:
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        return item

    async def create_cart_item(self, payload: CartItemCreate) -> CartItemOrm:
        item = CartItemOrm(
            cart_id=payload.cart_id,
            item_id=payload.item_id,
            quantity=payload.quantity,
            created_by=payload.created_by,
        )
        return await self.repo.create(item)

    async def update_cart_item(self, item_id: int, payload: CartItemUpdate) -> CartItemOrm:
        item = await self.get_cart_item(item_id)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        return await self.repo.update(item)

    async def delete_cart_item(self, item_id: int) -> None:
        item = await self.get_cart_item(item_id)
        await self.repo.soft_delete(item)
