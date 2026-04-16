from sqlalchemy import select
from sqlalchemy.orm import Session
from app.orm.users import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[User]:
        stmt = select(User).where(User.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.user_id == user_id, User.is_deleted.is_(False))
        return self.db.scalars(stmt).first()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email, User.is_deleted.is_(False))
        return self.db.scalars(stmt).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def soft_delete(self, user: User) -> None:
        user.is_deleted = True
        self.db.add(user)
        self.db.commit()
