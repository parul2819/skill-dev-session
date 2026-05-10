from app.core.logger import setup_logger
from app.core.exceptions.custom_exceptions import NotFoundException
from app.dto import CartItemCreate, CartItemUpdate
from app.orm import CartItemOrm
from app.repositories import CartItemRepository

logger = setup_logger()

class CartItemService:
    def __init__(self, repo: CartItemRepository) -> None:
        self.repo = repo

    async def list_cart_items(self) -> list[CartItemOrm]:
        return await self.repo.list_active()

    async def get_cart_item(self, cart_item_id: int) -> CartItemOrm:
        item = await self.repo.get_by_id(cart_item_id)
        if not item:
            logger.error(f"Cart item not found with ID: {cart_item_id}")
            raise NotFoundException(message="Cart item not found")
        return item

    async def create_cart_item(self, payload: CartItemCreate) -> CartItemOrm:
        item = CartItemOrm(
            cart_id=payload.cart_id,
            item_id=payload.item_id,
            quantity=payload.quantity,
            created_by=payload.created_by,
        )
        return await self.repo.create(item)

    async def update_cart_item(self, cart_item_id: int, payload: CartItemUpdate) -> CartItemOrm:
        item = await self.get_cart_item(cart_item_id)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        return await self.repo.update(item)

    async def delete_cart_item(self, cart_item_id: int) -> None:
        item = await self.get_cart_item(cart_item_id)
        await self.repo.soft_delete(item)
