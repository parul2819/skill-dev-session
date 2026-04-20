from fastapi import HTTPException, status
from app.dto import OrderCreate, OrderUpdate
from app.orm import OrderOrm
from app.repositories import OrderRepository


class OrderService:
    def __init__(self, repo: OrderRepository) -> None:
        self.repo = repo

    async def list_orders(self) -> list[OrderOrm]:
        return await self.repo.list_active()

    async def get_order(self, order_id: int) -> OrderOrm:
        order = await self.repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order

    async def create_order(self, payload: OrderCreate) -> OrderOrm:
        order = OrderOrm(
            user_id=payload.user_id,
            restaurant_id=payload.restaurant_id,
            offer_id=payload.offer_id,
            total_amount=payload.total_amount,
            discount_amount=payload.discount_amount,
            final_amount=payload.final_amount,
            order_status=payload.order_status,
        )
        return await self.repo.create(order)

    async def update_order(self, order_id: int, payload: OrderUpdate) -> OrderOrm:
        order = await self.get_order(order_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order, key, value)
        return await self.repo.update(order)

    async def delete_order(self, order_id: int) -> None:
        order = await self.get_order(order_id)
        await self.repo.soft_delete(order)
