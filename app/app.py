from fastapi import FastAPI
from app.api.controller.user_controller import router as user_router
from app.api.controller.restaurant_controller import router as restaurant_controller
from app.api.controller.menu_items_controller import router as menu_items_controller
from app.api.controller.offers_controller import router as offers_controller
from app.api.controller.cart_controller import router as cart_controller
from app.api.controller.cart_items_controller import router as cart_items_controller
from app.api.controller.orders_controller import router as orders_controller
from app.api.controller.order_items_controller import router as order_items_controller
from app.api.controller.order_ratings_controller import router as order_ratings_controller
from app.api.controller.user_addresses_controller import router as user_addresses_controller
from app.core.db.base import Base
from app.core.db.session import engine
import app.orm  # noqa: F401  # ensure all models are imported

app = FastAPI(title="Food Delivery API")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(user_router)
app.include_router(restaurant_controller)
app.include_router(menu_items_controller)
app.include_router(offers_controller)
app.include_router(cart_controller)
app.include_router(cart_items_controller)
app.include_router(orders_controller)
app.include_router(order_items_controller)
app.include_router(order_ratings_controller)
app.include_router(user_addresses_controller)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
