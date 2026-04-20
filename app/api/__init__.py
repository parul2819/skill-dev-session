from app.api.controller.cart_controller import router as cart_router
from app.api.controller.cart_items_controller import router as cart_items_router
from app.api.controller.menu_items_controller import router as menu_items_router
from app.api.controller.offers_controller import router as offers_router
from app.api.controller.order_items_controller import router as order_items_router
from app.api.controller.order_ratings_controller import router as order_ratings_router
from app.api.controller.orders_controller import router as orders_router
from app.api.controller.restaurant_controller import router as restaurant_router
from app.api.controller.user_addresses_controller import router as user_addresses_router
from app.api.controller.user_controller import router as user_router

__all__ = [
    "cart_router",
    "cart_items_router",
    "menu_items_router",
    "offers_router",
    "order_items_router",
    "order_ratings_router",
    "orders_router",
    "restaurant_router",
    "user_addresses_router",
    "user_router",
]