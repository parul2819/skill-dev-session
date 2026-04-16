from fastapi import HTTPException, status
from app.dto.user_addresses_dto import UserAddressCreate, UserAddressUpdate
from app.orm.user_addresses import UserAddress
from app.repositories.user_addresses_repository import UserAddressRepository

class UserAddressService:
    def __init__(self, repo: UserAddressRepository) -> None:
        self.repo = repo

    def list_addresses(self) -> list[UserAddress]:
        return self.repo.list_active()

    def get_address(self, address_id: int) -> UserAddress:
        address = self.repo.get_by_id(address_id)
        if not address:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        return address

    def list_user_addresses(self, user_id: int) -> list[UserAddress]:
        return self.repo.get_by_user_id(user_id)

    def create_address(self, payload: UserAddressCreate) -> UserAddress:
        if payload.is_default:
            self.repo.reset_default_for_user(payload.user_id)

        user_address = UserAddress(
            user_id=payload.user_id,
            address_line=payload.address_line,
            city=payload.city,
            state=payload.state,
            pincode=payload.pincode,
            is_default=payload.is_default
        )
        return self.repo.create(user_address)

    def update_address(self, address_id: int, payload: UserAddressUpdate) -> UserAddress:
        address = self.get_address(address_id)
        
        update_data = payload.model_dump(exclude_unset=True)
        
        if update_data.get("is_default"):
            user_id = update_data.get("user_id") or address.user_id
            self.repo.reset_default_for_user(user_id)

        for key, value in update_data.items():
            setattr(address, key, value)
            
        return self.repo.update(address)

    def delete_address(self, address_id: int) -> None:
        address = self.get_address(address_id)
        self.repo.soft_delete(address)
