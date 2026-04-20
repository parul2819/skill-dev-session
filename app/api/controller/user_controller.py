from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.core.db.get_db import get_db
from app.dto import UserCreate, UserRead, UserUpdate
from app.repositories import UserRepository
from app.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


@router.get("/", response_model=list[UserRead])
async def list_users(service: UserService = Depends(get_user_service)) -> Any:
    return await service.list_users()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)) -> Any:
    return await service.get_user(user_id)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)) -> Any:
    return await service.create_user(payload)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> Any:
    return await service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> None:
    await service.delete_user(user_id)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
