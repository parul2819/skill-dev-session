from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.core.db.get_db import get_db
from app.dto import CartCreate, CartRead, CartUpdate
from app.repositories import CartRepository
from app.services import CartService

router = APIRouter(prefix="/carts", tags=["Carts"])


async def get_cart_service(db: AsyncSession = Depends(get_db)) -> Any:
    repo = CartRepository(db)
    return CartService(repo)


@router.get("/", response_model=list[CartRead])
async def list_carts(service: CartService = Depends(get_cart_service)) -> Any:
    return await service.list_carts()


@router.get("/{cart_id}", response_model=CartRead)
async def get_cart(cart_id: int, service: CartService = Depends(get_cart_service)) -> Any:
    return await service.get_cart(cart_id)


@router.post("/", response_model=CartRead, status_code=status.HTTP_201_CREATED)
async def create_cart(payload: CartCreate, service: CartService = Depends(get_cart_service)) -> Any:
    return await service.create_cart(payload)


@router.put("/{cart_id}", response_model=CartRead)
async def update_cart(
    cart_id: int,
    payload: CartUpdate,
    service: CartService = Depends(get_cart_service),
) -> Any:
    return await service.update_cart(cart_id, payload)


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(cart_id: int, service: CartService = Depends(get_cart_service)) -> None:
    await service.delete_cart(cart_id)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
