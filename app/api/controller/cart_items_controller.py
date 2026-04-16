from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.db.get_db import get_db
from app.dto.cart_items_dto import CartItemCreate, CartItemRead, CartItemUpdate
from app.repositories.cart_items_repository import CartItemRepository
from app.services.cart_items_service import CartItemService

router = APIRouter(prefix="/cart-items", tags=["Cart Items"])


def get_cart_item_service(db: Session = Depends(get_db)) -> CartItemService:
    repo = CartItemRepository(db)
    return CartItemService(repo)


@router.get("/", response_model=list[CartItemRead])
def list_cart_items(service: CartItemService = Depends(get_cart_item_service)) -> list[CartItemRead]:
    return service.list_cart_items()


@router.get("/{item_id}", response_model=CartItemRead)
def get_cart_item(item_id: int, service: CartItemService = Depends(get_cart_item_service)) -> CartItemRead:
    return service.get_cart_item(item_id)


@router.post("/", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
def create_cart_item(
    payload: CartItemCreate, service: CartItemService = Depends(get_cart_item_service)
) -> CartItemRead:
    return service.create_cart_item(payload)


@router.put("/{item_id}", response_model=CartItemRead)
def update_cart_item(
    item_id: int,
    payload: CartItemUpdate,
    service: CartItemService = Depends(get_cart_item_service),
) -> CartItemRead:
    return service.update_cart_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(item_id: int, service: CartItemService = Depends(get_cart_item_service)) -> Response:
    service.delete_cart_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
