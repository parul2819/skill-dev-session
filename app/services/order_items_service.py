from fastapi import HTTPException, status
from app.dto.order_items_dto import OrderItemCreate, OrderItemUpdate
from app.orm.order_items import OrderItem
from app.repositories.order_items_repository import OrderItemRepository


class OrderItemService:
    def __init__(self, repo: OrderItemRepository) -> None:
        self.repo = repo

    def list_order_items(self) -> list[OrderItem]:
        return self.repo.list_active()

    def get_order_item(self, order_item_id: int) -> OrderItem:
        order_item = self.repo.get_by_id(order_item_id)
        if not order_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
        return order_item

    def list_order_items_by_order(self, order_id: int) -> list[OrderItem]:
        return self.repo.get_by_order_id(order_id)

    def create_order_item(self, payload: OrderItemCreate) -> OrderItem:
        order_item = OrderItem(
            order_id=payload.order_id,
            item_id=payload.item_id,
            quantity=payload.quantity,
            price=payload.price,
        )
        return self.repo.create(order_item)

    def update_order_item(self, order_item_id: int, payload: OrderItemUpdate) -> OrderItem:
        order_item = self.get_order_item(order_item_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order_item, key, value)
        return self.repo.update(order_item)

    def delete_order_item(self, order_item_id: int) -> None:
        order_item = self.get_order_item(order_item_id)
        self.repo.soft_delete(order_item)
