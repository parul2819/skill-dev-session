from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.core.db.get_db import get_db
from app.dto import MenuItemCreate, MenuItemRead, MenuItemUpdate
from app.repositories import MenuItemRepository
from app.services import MenuItemService

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])


async def get_menu_item_service(db: AsyncSession = Depends(get_db)) -> Any:
    repo = MenuItemRepository(db)
    return MenuItemService(repo)


@router.get("/", response_model=list[MenuItemRead])
async def list_menu_items(service: MenuItemService = Depends(get_menu_item_service)) -> Any:
    return await service.list_menu_items()


@router.get("/{item_id}", response_model=MenuItemRead)
async def get_menu_item(item_id: int, service: MenuItemService = Depends(get_menu_item_service)) -> Any:
    return await service.get_menu_item(item_id)


@router.post("/", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
async def create_menu_item(payload: MenuItemCreate, service: MenuItemService = Depends(get_menu_item_service)) -> Any:
    return await service.create_menu_item(payload)


@router.put("/{item_id}", response_model=MenuItemRead)
async def update_menu_item(
    item_id: int,
    payload: MenuItemUpdate,
    service: MenuItemService = Depends(get_menu_item_service),
) -> Any:
    return await service.update_menu_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(item_id: int, service: MenuItemService = Depends(get_menu_item_service)) -> None:
    await service.delete_menu_item(item_id)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
