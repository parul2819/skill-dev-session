import logging
from fastapi import HTTPException, status
from app.core.exceptions.custom_exceptions import NotFoundException
from app.dto import UserCreate, UserUpdate
from app.orm import UserOrm
from app.repositories import UserRepository

logger = logging.getLogger("app.services.user_service")

class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def list_users(self) -> list[UserOrm]:
        logger.info("Listing all active users")
        return await self.repo.list_active()

    async def get_user(self, user_id: int) -> UserOrm:
        logger.info(f"Fetching user details for ID: {user_id}")
        user = await self.repo.get_by_id(user_id)
        if not user:
            logger.error(f"User not found with ID: {user_id}")
            raise NotFoundException()

        return user

    async def create_user(self, payload: UserCreate) -> UserOrm:
        logger.info(f"Attempting to create user with email: {payload.email}")
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            logger.error(f"Email conflict: {payload.email} already exists")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        user = UserOrm(
            name=payload.name,
            email=payload.email,
            password=payload.password,
            phone_number=payload.phone_number,
        )
        return await self.repo.create(user)

    async def update_user(self, user_id: int, payload: UserUpdate) -> UserOrm:
        logger.info(f"Updating user with ID: {user_id}")
        user = await self.get_user(user_id)
        if not user:
            logger.error(f"Update failed: User with ID {user_id} not found")
            raise NotFoundException()

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        return await self.repo.update(user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user(user_id)
        await self.repo.soft_delete(user)
