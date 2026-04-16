from fastapi import HTTPException, status
from app.dto.orders_dto import OrderCreate, OrderUpdate
from app.orm.orders import Order
from app.repositories.orders_repository import OrderRepository


class OrderService:
    def __init__(self, repo: OrderRepository) -> None:
        self.repo = repo

    def list_orders(self) -> list[Order]:
        return self.repo.list_active()

    def get_order(self, order_id: int) -> Order:
        order = self.repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return order

    def create_order(self, payload: OrderCreate) -> Order:
        order = Order(
            user_id=payload.user_id,
            restaurant_id=payload.restaurant_id,
            offer_id=payload.offer_id,
            total_amount=payload.total_amount,
            discount_amount=payload.discount_amount,
            final_amount=payload.final_amount,
            order_status=payload.order_status,
        )
        return self.repo.create(order)

    def update_order(self, order_id: int, payload: OrderUpdate) -> Order:
        order = self.get_order(order_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order, key, value)
        return self.repo.update(order)

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        self.repo.soft_delete(order)
