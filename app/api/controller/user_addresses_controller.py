from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.db.get_db import get_db
from app.dto.user_addresses_dto import UserAddressCreate, UserAddressRead, UserAddressUpdate
from app.repositories.user_addresses_repository import UserAddressRepository
from app.services.user_addresses_service import UserAddressService

router = APIRouter(prefix="/user-addresses", tags=["User Addresses"])


def get_user_address_service(db: Session = Depends(get_db)) -> UserAddressService:
    repo = UserAddressRepository(db)
    return UserAddressService(repo)


@router.get("/", response_model=list[UserAddressRead])
def list_addresses(service: UserAddressService = Depends(get_user_address_service)):
    return service.list_addresses()


@router.get("/{address_id}", response_model=UserAddressRead)
def get_address(address_id: int, service: UserAddressService = Depends(get_user_address_service)):
    return service.get_address(address_id)


@router.get("/user/{user_id}", response_model=list[UserAddressRead])
def list_user_addresses(user_id: int, service: UserAddressService = Depends(get_user_address_service)):
    return service.list_user_addresses(user_id)


@router.post("/", response_model=UserAddressRead, status_code=status.HTTP_201_CREATED)
def create_address(payload: UserAddressCreate, service: UserAddressService = Depends(get_user_address_service)):
    return service.create_address(payload)


@router.patch("/{address_id}", response_model=UserAddressRead)
def update_address(
    address_id: int, payload: UserAddressUpdate, service: UserAddressService = Depends(get_user_address_service)
):
    return service.update_address(address_id, payload)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, service: UserAddressService = Depends(get_user_address_service)):
    service.delete_address(address_id)
