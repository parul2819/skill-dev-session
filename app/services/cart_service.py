from fastapi import HTTPException, status

from app.dto import CartCreate, CartUpdate
from app.orm import CartOrm
from app.repositories import CartRepository


class CartService:
    def __init__(self, repo: CartRepository) -> None:
        self.repo = repo

    async def list_carts(self) -> list[CartOrm]:
        return await self.repo.list_active()

    async def get_cart(self, cart_id: int) -> CartOrm:
        cart = await self.repo.get_by_id(cart_id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
        return cart

    async def create_cart(self, payload: CartCreate) -> CartOrm:
        existing = await self.repo.get_by_user_id(payload.user_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cart already exists for user")

        cart = CartOrm(
            user_id=payload.user_id,
            restaurant_id=payload.restaurant_id,
        )
        return await self.repo.create(cart)

    async def update_cart(self, cart_id: int, payload: CartUpdate) -> CartOrm:
        cart = await self.get_cart(cart_id)

        update_data = payload.model_dump(exclude_unset=True)
        if "user_id" in update_data and update_data["user_id"] != cart.user_id:
            existing = self.repo.get_by_user_id(update_data["user_id"])
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cart already exists for user")

        for key, value in update_data.items():
            setattr(cart, key, value)

        return await self.repo.update(cart)

    async def delete_cart(self, cart_id: int) -> None:
        cart = await self.get_cart(cart_id)
        await self.repo.soft_delete(cart)
