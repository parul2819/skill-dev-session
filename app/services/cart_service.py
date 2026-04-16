from fastapi import HTTPException, status

from app.dto.cart_dto import CartCreate, CartUpdate
from app.orm.cart import Cart
from app.repositories.cart_repository import CartRepository


class CartService:
    def __init__(self, repo: CartRepository) -> None:
        self.repo = repo

    def list_carts(self) -> list[Cart]:
        return self.repo.list_active()

    def get_cart(self, cart_id: int) -> Cart:
        cart = self.repo.get_by_id(cart_id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
        return cart

    def create_cart(self, payload: CartCreate) -> Cart:
        existing = self.repo.get_by_user_id(payload.user_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cart already exists for user")

        cart = Cart(
            user_id=payload.user_id,
            restaurant_id=payload.restaurant_id,
        )
        return self.repo.create(cart)

    def update_cart(self, cart_id: int, payload: CartUpdate) -> Cart:
        cart = self.get_cart(cart_id)

        update_data = payload.model_dump(exclude_unset=True)
        if "user_id" in update_data and update_data["user_id"] != cart.user_id:
            existing = self.repo.get_by_user_id(update_data["user_id"])
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cart already exists for user")

        for key, value in update_data.items():
            setattr(cart, key, value)

        return self.repo.update(cart)

    def delete_cart(self, cart_id: int) -> None:
        cart = self.get_cart(cart_id)
        self.repo.soft_delete(cart)
