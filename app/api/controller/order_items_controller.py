from fastapi import APIRouter, Depends, status
from typing import Any
from sqlalchemy.orm import Session
from app.core.db.get_db import get_db
from app.dto.order_items_dto import OrderItemCreate, OrderItemRead, OrderItemUpdate
from app.repositories.order_items_repository import OrderItemRepository
from app.services.order_items_service import OrderItemService

router = APIRouter(prefix="/order-items", tags=["Order Items"])


def get_order_item_service(db: Session = Depends(get_db)) -> Any:
    repo = OrderItemRepository(db)
    return OrderItemService(repo)


@router.get("/", response_model=list[OrderItemRead])
def list_order_items(service: OrderItemService = Depends(get_order_item_service)) -> Any:
    return service.list_order_items()


@router.get("/{order_item_id}", response_model=OrderItemRead)
def get_order_item(order_item_id: int, service: OrderItemService = Depends(get_order_item_service)) -> Any:
    return service.get_order_item(order_item_id)


@router.get("/order/{order_id}", response_model=list[OrderItemRead])
def list_order_items_by_order(order_id: int, service: OrderItemService = Depends(get_order_item_service)) -> Any:
    return service.list_order_items_by_order(order_id)


@router.post("/", response_model=OrderItemRead, status_code=status.HTTP_201_CREATED)
def create_order_item(payload: OrderItemCreate, service: OrderItemService = Depends(get_order_item_service)) -> Any:
    return service.create_order_item(payload)


@router.patch("/{order_item_id}", response_model=OrderItemRead)
def update_order_item(
    order_item_id: int, payload: OrderItemUpdate, service: OrderItemService = Depends(get_order_item_service)
) -> Any:
    return service.update_order_item(order_item_id, payload)


@router.delete("/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(order_item_id: int, service: OrderItemService = Depends(get_order_item_service)) -> Any:
    service.delete_order_item(order_item_id)
