from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from typing import Any
from app.core.db.get_db import get_db
from app.dto.cart_dto import CartCreate, CartRead, CartUpdate
from app.repositories.cart_repository import CartRepository
from app.services.cart_service import CartService

router = APIRouter(prefix="/carts", tags=["Carts"])


def get_cart_service(db: Session = Depends(get_db)) -> Any:
    repo = CartRepository(db)
    return CartService(repo)


@router.get("/", response_model=list[CartRead])
def list_carts(service: CartService = Depends(get_cart_service)) -> Any:
    return service.list_carts()


@router.get("/{cart_id}", response_model=CartRead)
def get_cart(cart_id: int, service: CartService = Depends(get_cart_service)) -> Any:
    return service.get_cart(cart_id)


@router.post("/", response_model=CartRead, status_code=status.HTTP_201_CREATED)
def create_cart(payload: CartCreate, service: CartService = Depends(get_cart_service)) -> Any:
    return service.create_cart(payload)


@router.put("/{cart_id}", response_model=CartRead)
def update_cart(
    cart_id: int,
    payload: CartUpdate,
    service: CartService = Depends(get_cart_service),
) -> Any:
    return service.update_cart(cart_id, payload)


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(cart_id: int, service: CartService = Depends(get_cart_service)) -> None:
    service.delete_cart(cart_id)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
