from fastapi import HTTPException, status
from app.dto import OrderItemCreate, OrderItemUpdate
from app.orm import OrderItemOrm
from app.repositories import OrderItemRepository


class OrderItemService:
    def __init__(self, repo: OrderItemRepository) -> None:
        self.repo = repo

    async def list_order_items(self) -> list[OrderItemOrm]:
        return await self.repo.list_active()

    async def get_order_item(self, order_item_id: int) -> OrderItemOrm:
        order_item = await self.repo.get_by_id(order_item_id)
        if not order_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
        return order_item

    async def list_order_items_by_order(self, order_id: int) -> list[OrderItemOrm]:
        return await self.repo.get_by_order_id(order_id)

    async def create_order_item(self, payload: OrderItemCreate) -> OrderItemOrm:
        order_item = OrderItemOrm(
            order_id=payload.order_id,
            item_id=payload.item_id,
            quantity=payload.quantity,
            price=payload.price,
        )
        return await self.repo.create(order_item)

    async def update_order_item(self, order_item_id: int, payload: OrderItemUpdate) -> OrderItemOrm:
        order_item = await self.get_order_item(order_item_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order_item, key, value)
        return await self.repo.update(order_item)

    async def delete_order_item(self, order_item_id: int) -> None:
        order_item = await self.get_order_item(order_item_id)
        await self.repo.soft_delete(order_item)
