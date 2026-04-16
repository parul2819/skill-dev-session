from fastapi import HTTPException, status

from app.dto.user_dto import UserCreate, UserUpdate
from app.orm.users import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def list_users(self) -> list[User]:
        return self.repo.list_active()

    def get_user(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def create_user(self, payload: UserCreate) -> User:
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        user = User(
            name=payload.name,
            email=payload.email,
            password=payload.password,
            phone_number=payload.phone_number,
        )
        return self.repo.create(user)

    def update_user(self, user_id: int, payload: UserUpdate) -> User:
        user = self.get_user(user_id)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        return self.repo.update(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repo.soft_delete(user)