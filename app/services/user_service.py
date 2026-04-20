from fastapi import HTTPException, status

from app.dto import UserCreate, UserUpdate
from app.orm import UserOrm
from app.repositories import UserRepository


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def list_users(self) -> list[UserOrm]:
        return await self.repo.list_active()

    async def get_user(self, user_id: int) -> UserOrm:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def create_user(self, payload: UserCreate) -> UserOrm:
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        user = UserOrm(
            name=payload.name,
            email=payload.email,
            password=payload.password,
            phone_number=payload.phone_number,
        )
        return await self.repo.create(user)

    async def update_user(self, user_id: int, payload: UserUpdate) -> UserOrm:
        user = await self.get_user(user_id)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        return await self.repo.update(user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user(user_id)
        await self.repo.soft_delete(user)
