from fastapi import HTTPException, status
from app.dto import UserAddressCreate, UserAddressUpdate
from app.orm import UserAddressOrm
from app.repositories import UserAddressRepository


class UserAddressService:
    def __init__(self, repo: UserAddressRepository) -> None:
        self.repo = repo

    async def list_addresses(self) -> list[UserAddressOrm]:
        return await self.repo.list_active()

    async def get_address(self, address_id: int) -> UserAddressOrm:
        address = await self.repo.get_by_id(address_id)
        if not address:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        return address

    async def list_user_addresses(self, user_id: int) -> list[UserAddressOrm]:
        return await self.repo.get_by_user_id(user_id)

    async def create_address(self, payload: UserAddressCreate) -> UserAddressOrm:
        if payload.is_default:
            await self.repo.reset_default_for_user(payload.user_id)

        user_address = UserAddress(
            user_id=payload.user_id,
            address_line=payload.address_line,
            city=payload.city,
            state=payload.state,
            pincode=payload.pincode,
            is_default=payload.is_default,
        )
        return await self.repo.create(user_address)

    async def update_address(self, address_id: int, payload: UserAddressUpdate) -> UserAddressOrm:
        address = await self.get_address(address_id)

        update_data = payload.model_dump(exclude_unset=True)

        if update_data.get("is_default"):
            user_id = update_data.get("user_id") or address.user_id
            await self.repo.reset_default_for_user(user_id)

        for key, value in update_data.items():
            setattr(address, key, value)

        return await self.repo.update(address)

    async def delete_address(self, address_id: int) -> None:
        address = await self.get_address(address_id)
        await self.repo.soft_delete(address)
