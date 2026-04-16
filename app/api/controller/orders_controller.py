from fastapi import APIRouter, Depends, status
from typing import Any
from sqlalchemy.orm import Session
from app.core.db.get_db import get_db
from app.dto.orders_dto import OrderCreate, OrderRead, OrderUpdate
from app.repositories.orders_repository import OrderRepository
from app.services.orders_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_order_service(db: Session = Depends(get_db)) -> Any:
    repo = OrderRepository(db)
    return OrderService(repo)


@router.get("/", response_model=list[OrderRead])
def list_orders(service: OrderService = Depends(get_order_service)) -> Any:
    return service.list_orders()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, service: OrderService = Depends(get_order_service)) -> Any:
    return service.get_order(order_id)


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, service: OrderService = Depends(get_order_service)) -> Any:
    return service.create_order(payload)


@router.patch("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, payload: OrderUpdate, service: OrderService = Depends(get_order_service)) -> Any:
    return service.update_order(order_id, payload)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, service: OrderService = Depends(get_order_service)) -> Any:
    service.delete_order(order_id)
