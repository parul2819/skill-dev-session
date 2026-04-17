from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from typing import Any
from app.core.db.get_db import get_db
from app.dto.user_dto import UserCreate, UserRead, UserUpdate
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


@router.get("/", response_model=list[UserRead])
def list_users(service: UserService = Depends(get_user_service)) -> Any:
    return service.list_users()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)) -> Any:
    return service.get_user(user_id)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)) -> Any:
    return service.create_user(payload)


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> Any:
    return service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> None:
    service.delete_user(user_id)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
