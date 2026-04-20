from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.core.db.get_db import get_db
from app.dto import CartItemCreate, CartItemRead, CartItemUpdate
from app.repositories import CartItemRepository
from app.services import CartItemService

router = APIRouter(prefix="/cart-items", tags=["Cart Items"])


async def get_cart_item_service(db: AsyncSession = Depends(get_db)) -> Any:
    repo = CartItemRepository(db)
    return CartItemService(repo)


@router.get("/", response_model=list[CartItemRead])
async def list_cart_items(service: CartItemService = Depends(get_cart_item_service)) -> Any:
    return await service.list_cart_items()


@router.get("/{item_id}", response_model=CartItemRead)
async def get_cart_item(item_id: int, service: CartItemService = Depends(get_cart_item_service)) -> Any:
    return await service.get_cart_item(item_id)


@router.post("/", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
async def create_cart_item(payload: CartItemCreate, service: CartItemService = Depends(get_cart_item_service)) -> Any:
    return await service.create_cart_item(payload)


@router.put("/{item_id}", response_model=CartItemRead)
async def update_cart_item(
    item_id: int,
    payload: CartItemUpdate,
    service: CartItemService = Depends(get_cart_item_service),
) -> Any:
    return await service.update_cart_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(item_id: int, service: CartItemService = Depends(get_cart_item_service)) -> None:
    await service.delete_cart_item(item_id)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
