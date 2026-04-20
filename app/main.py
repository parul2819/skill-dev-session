from fastapi import FastAPI
from app.api import (cart_router, cart_items_router, menu_items_router,
                                offers_router, order_items_router, order_ratings_router,
                                orders_router, restaurant_router, user_addresses_router,
                                user_router)

from app.core.db.base import Base
from app.core.db.session import engine
import app.orm  # noqa: F401  # ensure all models are imported

delivery_app = FastAPI(title="Food Delivery API")


@delivery_app.on_event("startup")
def on_startup() -> None:
    # Base.metadata.create_all(bind=engine)
    pass


delivery_app.include_router(user_router)
delivery_app.include_router(restaurant_router)
delivery_app.include_router(menu_items_router)
delivery_app.include_router(offers_router)
delivery_app.include_router(cart_router)
delivery_app.include_router(cart_items_router)
delivery_app.include_router(orders_router)
delivery_app.include_router(order_items_router)
delivery_app.include_router(order_ratings_router)
delivery_app.include_router(user_addresses_router)


@delivery_app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
