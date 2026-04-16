from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.orm.user_addresses import UserAddress


class UserAddressRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[UserAddress]:
        stmt = select(UserAddress).where(UserAddress.is_deleted.is_(False))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, address_id: int) -> UserAddress | None:
        stmt = select(UserAddress).where(
            UserAddress.address_id == address_id,
            UserAddress.is_deleted.is_(False),
        )
        return self.db.scalars(stmt).first()

    def get_by_user_id(self, user_id: int) -> list[UserAddress]:
        stmt = select(UserAddress).where(
            UserAddress.user_id == user_id,
            UserAddress.is_deleted.is_(False),
        )
        return list(self.db.scalars(stmt).all())

    def reset_default_for_user(self, user_id: int) -> None:
        stmt = (
            update(UserAddress)
            .where(UserAddress.user_id == user_id, UserAddress.is_default.is_(True))
            .values(is_default=False)
        )
        self.db.execute(stmt)
        self.db.commit()

    def create(self, user_address: UserAddress) -> UserAddress:
        self.db.add(user_address)
        self.db.commit()
        self.db.refresh(user_address)
        return user_address

    def update(self, user_address: UserAddress) -> UserAddress:
        self.db.add(user_address)
        self.db.commit()
        self.db.refresh(user_address)
        return user_address

    def soft_delete(self, user_address: UserAddress) -> None:
        user_address.is_deleted = True
        self.db.add(user_address)
        self.db.commit()
