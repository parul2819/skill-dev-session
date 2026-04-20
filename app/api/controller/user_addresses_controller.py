from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.get_db import get_db
from app.dto import UserAddressCreate, UserAddressRead, UserAddressUpdate
from app.repositories import UserAddressRepository
from app.services import UserAddressService

router = APIRouter(prefix="/user-addresses", tags=["User Addresses"])


async def get_user_address_service(db: AsyncSession = Depends(get_db)) -> Any:
    repo = UserAddressRepository(db)
    return UserAddressService(repo)


@router.get("/", response_model=list[UserAddressRead])
async def list_addresses(service: UserAddressService = Depends(get_user_address_service)) -> Any:
    return await service.list_addresses()


@router.get("/{address_id}", response_model=UserAddressRead)
async def get_address(address_id: int, service: UserAddressService = Depends(get_user_address_service)) -> Any:
    return await service.get_address(address_id)


@router.get("/user/{user_id}", response_model=list[UserAddressRead])
async def list_user_addresses(user_id: int, service: UserAddressService = Depends(get_user_address_service)) -> Any:
    return await service.list_user_addresses(user_id)


@router.post("/", response_model=UserAddressRead, status_code=status.HTTP_201_CREATED)
async def create_address(payload: UserAddressCreate, service: UserAddressService = Depends(get_user_address_service)) -> Any:
    return await service.create_address(payload)


@router.patch("/{address_id}", response_model=UserAddressRead)
async def update_address(
    address_id: int, payload: UserAddressUpdate, service: UserAddressService = Depends(get_user_address_service)
) -> Any:
    return await service.update_address(address_id, payload)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: int, service: UserAddressService = Depends(get_user_address_service)) -> None:
    await service.delete_address(address_id)
