from fastapi import APIRouter, Depends, status
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.get_db import get_db
from app.dto import OrderCreate, OrderRead, OrderUpdate
from app.repositories import OrderRepository
from app.services import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


async def get_order_service(db: AsyncSession = Depends(get_db)) -> Any:
    repo = OrderRepository(db)
    return OrderService(repo)


@router.get("/", response_model=list[OrderRead])
async def list_orders(service: OrderService = Depends(get_order_service)) -> Any:
    return await service.list_orders()


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, service: OrderService = Depends(get_order_service)) -> Any:
    return await service.get_order(order_id)


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate, service: OrderService = Depends(get_order_service)) -> Any:
    return await service.create_order(payload)


@router.patch("/{order_id}", response_model=OrderRead)
async def update_order(order_id: int, payload: OrderUpdate, service: OrderService = Depends(get_order_service)) -> Any:
    return await service.update_order(order_id, payload)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, service: OrderService = Depends(get_order_service)) -> None:
    await service.delete_order(order_id)
