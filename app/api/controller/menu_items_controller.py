from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from typing import Any
from app.core.db.get_db import get_db
from app.dto.menu_items_dto import MenuItemCreate, MenuItemRead, MenuItemUpdate
from app.repositories.menu_items_repository import MenuItemRepository
from app.services.menu_items_service import MenuItemService

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])


def get_menu_item_service(db: Session = Depends(get_db)) -> Any:
    repo = MenuItemRepository(db)
    return MenuItemService(repo)


@router.get("/", response_model=list[MenuItemRead])
def list_menu_items(service: MenuItemService = Depends(get_menu_item_service)) -> Any:
    return service.list_menu_items()


@router.get("/{item_id}", response_model=MenuItemRead)
def get_menu_item(item_id: int, service: MenuItemService = Depends(get_menu_item_service)) -> Any:
    return service.get_menu_item(item_id)


@router.post("/", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
def create_menu_item(payload: MenuItemCreate, service: MenuItemService = Depends(get_menu_item_service)) -> Any:
    return service.create_menu_item(payload)


@router.put("/{item_id}", response_model=MenuItemRead)
def update_menu_item(
    item_id: int,
    payload: MenuItemUpdate,
    service: MenuItemService = Depends(get_menu_item_service),
) -> Any:
    return service.update_menu_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(item_id: int, service: MenuItemService = Depends(get_menu_item_service)) -> None:
    service.delete_menu_item(item_id)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
